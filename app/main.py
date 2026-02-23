from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
import uuid

from app.dataset_manager import get_dataset_manager
from app.ml_service_dynamic import predict_all_records, get_record_analysis
from app.advisor import handle_query
from app.schemas import AdvisorRequest, AdvisorResponse


# ── Lifespan ───────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize dataset manager on startup."""
    print("Initializing Dataset Manager...")
    get_dataset_manager()
    print("Ready!")
    yield


# ── App ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Dynamic Student Result Analysis — GenAI Academic Advisor",
    description=(
        "A flexible system that works with any CSV dataset to predict outcomes "
        "and provide AI-powered advising via Groq LLaMA."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoints ──────────────────────────────────────────────────────────

@app.post("/upload_csv")
async def upload_csv(
    file: UploadFile = File(...),
    dataset_id: str = None
):
    """
    Upload a CSV file to create a new dataset and train a model.
    
    The system will automatically:
    - Detect ID, target, and feature columns
    - Train a RandomForest classifier
    - Store the dataset and model for future queries
    
    Parameters:
    - file: CSV file to upload
    - dataset_id: Optional custom ID (auto-generated if not provided)
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    # Generate dataset ID if not provided
    if dataset_id is None:
        dataset_id = f"dataset_{uuid.uuid4().hex[:8]}"
    
    # Save uploaded file temporarily
    temp_path = Path("temp_upload.csv")
    try:
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the dataset
        manager = get_dataset_manager()
        result = manager.upload_dataset(str(temp_path), dataset_id)
        
        return {
            "success": True,
            "message": f"Dataset '{dataset_id}' uploaded and model trained successfully",
            "details": result
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing dataset: {str(e)}")
    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()


@app.get("/datasets")
async def list_datasets():
    """List all uploaded datasets with their metadata."""
    manager = get_dataset_manager()
    datasets = manager.list_datasets()
    return {
        "total": len(datasets),
        "datasets": datasets
    }


@app.delete("/datasets/{dataset_id}")
async def delete_dataset(dataset_id: str):
    """Delete a dataset and its trained model."""
    try:
        manager = get_dataset_manager()
        manager.delete_dataset(dataset_id)
        return {
            "success": True,
            "message": f"Dataset '{dataset_id}' deleted successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/ask_advisor", response_model=AdvisorResponse)
async def ask_advisor(request: AdvisorRequest):
    """
    Ask the GenAI Advisor a question about a specific dataset.

    Supports queries like:
    - "Which records need intervention?"
    - "Why is record 101 at risk?"
    - "Generate quiz for record 101"
    - Any general question about the data
    
    Parameters:
    - query: Your question
    - dataset_id: Which dataset to query (default: "default")
    """
    try:
        # Check if dataset exists
        manager = get_dataset_manager()
        if request.dataset_id not in manager.datasets:
            # Get list of available datasets
            available = list(manager.datasets.keys())
            if not available:
                return AdvisorResponse(
                    response_type="error",
                    message="No datasets have been uploaded yet. Please upload a CSV file first using the /upload_csv endpoint.",
                    data={"available_datasets": []}
                )
            else:
                return AdvisorResponse(
                    response_type="error",
                    message=f"Dataset '{request.dataset_id}' not found. Available datasets: {', '.join(available)}. Please upload a dataset with ID '{request.dataset_id}' or use one of the available datasets.",
                    data={"available_datasets": available}
                )
        
        return handle_query(request.query, request.dataset_id)
    except RuntimeError as e:
        return JSONResponse(
            status_code=429,
            content={
                "response_type": "error",
                "message": str(e),
                "data": None,
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "response_type": "error",
                "message": f"An unexpected error occurred: {str(e)}",
                "data": None,
            },
        )


@app.get("/records/{dataset_id}")
async def list_records(dataset_id: str):
    """Return all records with their predictions and risk analysis for a dataset."""
    try:
        results = predict_all_records(dataset_id)
        return {
            "dataset_id": dataset_id,
            "total": len(results),
            "records": results,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/records/{dataset_id}/{record_id}")
async def get_record(dataset_id: str, record_id: int):
    """Return detailed analysis for a single record in a dataset."""
    try:
        analysis = get_record_analysis(dataset_id, record_id)
        if analysis is None:
            raise HTTPException(status_code=404, detail=f"Record {record_id} not found in dataset '{dataset_id}'")
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint to verify system status."""
    manager = get_dataset_manager()
    datasets = manager.list_datasets()
    return {
        "status": "healthy",
        "datasets_count": len(datasets),
        "datasets": [d["dataset_id"] for d in datasets]
    }


@app.get("/")
async def root():
    manager = get_dataset_manager()
    datasets = manager.list_datasets()
    
    return {
        "service": "Dynamic Student Result Analysis — GenAI Academic Advisor",
        "version": "2.0.0",
        "description": "Upload any CSV and get AI-powered predictions and insights",
        "status": "ready",
        "datasets_uploaded": len(datasets),
        "available_datasets": [d["dataset_id"] for d in datasets],
        "endpoints": {
            "POST /upload_csv": "Upload a CSV file and train a model",
            "GET /datasets": "List all uploaded datasets",
            "DELETE /datasets/{id}": "Delete a dataset",
            "POST /ask_advisor": "Ask the AI advisor a question",
            "GET /records/{dataset_id}": "List all records with predictions",
            "GET /records/{dataset_id}/{record_id}": "Get analysis for a specific record",
            "GET /health": "Check system health and available datasets"
        },
    }
