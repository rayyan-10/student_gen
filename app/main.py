from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.ml_service import load_model, load_students, predict_all_students, get_student_analysis
from app.advisor import handle_query
from app.schemas import AdvisorRequest, AdvisorResponse


# ── Lifespan ───────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML model and student data on startup."""
    print("Loading ML model and student data...")
    load_model()
    load_students()
    print("Ready!")
    yield


# ── App ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Student Result Analysis — GenAI Academic Advisor",
    description=(
        "A system that predicts student pass/fail risk using a trained "
        "RandomForest model and provides AI-powered academic advising "
        "via Google Gemini."
    ),
    version="1.0.0",
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

@app.post("/ask_advisor", response_model=AdvisorResponse)
async def ask_advisor(request: AdvisorRequest):
    """
    Ask the GenAI Academic Advisor a question.

    Supports queries like:
    - "Which students need intervention?"
    - "Why is student S101 at risk?"
    - "Generate quiz for student S101"
    - Any general academic question
    """
    try:
        return handle_query(request.query)
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


@app.get("/students")
async def list_students():
    """Return all students with their predictions and risk analysis."""
    results = predict_all_students()
    return {
        "total": len(results),
        "students": results,
    }


@app.get("/students/{student_id}")
async def get_student(student_id: int):
    """Return detailed analysis for a single student."""
    analysis = get_student_analysis(student_id)
    if analysis is None:
        return {"error": f"Student {student_id} not found."}
    return analysis


@app.get("/")
async def root():
    return {
        "service": "Student Result Analysis — GenAI Academic Advisor",
        "version": "1.0.0",
        "endpoints": {
            "POST /ask_advisor": "Ask the AI advisor a question",
            "GET /students": "List all students with predictions",
            "GET /students/{id}": "Get analysis for a specific student",
        },
    }
