# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User / Client                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                         │
│                        (app/main.py)                             │
│                                                                   │
│  Endpoints:                                                       │
│  • POST /upload_csv          • GET /datasets                     │
│  • POST /ask_advisor         • DELETE /datasets/{id}             │
│  • GET /records/{dataset_id} • GET /records/{dataset_id}/{id}    │
└───────────┬─────────────────────────────┬───────────────────────┘
            │                             │
            │                             │
            ▼                             ▼
┌───────────────────────┐     ┌──────────────────────────────────┐
│   Dataset Manager     │     │      AI Advisor                  │
│ (dataset_manager.py)  │     │     (advisor.py)                 │
│                       │     │                                  │
│ • Upload CSV          │     │ • Query Classification           │
│ • Auto-detect columns │     │ • Intervention Analysis          │
│ • Train models        │     │ • Risk Explanation               │
│ • Store metadata      │     │ • Quiz Generation                │
│ • Manage multiple DS  │     │ • General Q&A                    │
└───────────┬───────────┘     └────────────┬─────────────────────┘
            │                              │
            │                              │
            ▼                              ▼
┌───────────────────────┐     ┌──────────────────────────────────┐
│  ML Service Dynamic   │     │      Groq API (LLaMA 3.3)        │
│ (ml_service_dynamic)  │     │                                  │
│                       │     │ • Natural language understanding │
│ • Predict all records │     │ • Risk factor analysis           │
│ • Analyze single rec  │     │ • Quiz generation                │
│ • Risk classification │     │ • Recommendations                │
│ • Weak area detection │     │ • Structured JSON responses      │
└───────────┬───────────┘     └──────────────────────────────────┘
            │
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Storage Layer                                 │
│                                                                   │
│  uploads/                    models/                             │
│  ├── dataset1.csv           ├── dataset1.pkl                     │
│  ├── dataset2.csv           ├── dataset2.pkl                     │
│  └── metadata.json          └── dataset3.pkl                     │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. CSV Upload Flow

```
User uploads CSV
      │
      ▼
FastAPI receives file
      │
      ▼
Dataset Manager
      │
      ├─► Detect columns (ID, target, features, topics)
      │
      ├─► Save CSV to uploads/
      │
      ├─► Train RandomForest model
      │
      ├─► Save model to models/
      │
      └─► Store metadata in metadata.json
      │
      ▼
Return success + column info + accuracy
```

### 2. Query Flow

```
User asks question
      │
      ▼
FastAPI /ask_advisor endpoint
      │
      ▼
AI Advisor
      │
      ├─► Classify query intent
      │   (intervention / student_risk / generate_quiz / general)
      │
      ├─► Extract record ID (if needed)
      │
      ▼
ML Service Dynamic
      │
      ├─► Load dataset from uploads/
      │
      ├─► Load model from models/
      │
      ├─► Run predictions
      │
      ├─► Classify risk levels
      │
      └─► Detect weak areas
      │
      ▼
AI Advisor
      │
      ├─► Build context prompt
      │
      ▼
Groq API (LLaMA)
      │
      ├─► Generate insights
      │
      └─► Return structured JSON
      │
      ▼
FastAPI formats response
      │
      ▼
Return to user
```

### 3. Prediction Flow

```
Request predictions for dataset
      │
      ▼
ML Service Dynamic
      │
      ├─► Get dataset from Dataset Manager
      │
      ├─► Get model from Dataset Manager
      │
      ├─► Get column info from Dataset Manager
      │
      ▼
For each record:
      │
      ├─► Extract features dynamically
      │
      ├─► Run model.predict_proba()
      │
      ├─► Classify risk (HIGH/MEDIUM/LOW)
      │
      ├─► Detect weak areas (scores < 50)
      │
      └─► Build result dict
      │
      ▼
Return all predictions
```

## Component Details

### Dataset Manager
**Responsibilities:**
- CSV upload handling
- Column auto-detection
- Model training orchestration
- Metadata persistence
- Multi-dataset management

**Key Methods:**
- `upload_dataset()` - Process new CSV
- `get_model()` - Retrieve trained model
- `get_dataframe()` - Load dataset
- `get_column_info()` - Get column metadata
- `list_datasets()` - List all datasets
- `delete_dataset()` - Remove dataset

### ML Service Dynamic
**Responsibilities:**
- Dynamic feature extraction
- Risk prediction
- Weak area identification
- Works with any column structure

**Key Methods:**
- `predict_all_records()` - Batch predictions
- `get_record_analysis()` - Single record analysis
- `get_high_risk_records()` - Filter high-risk
- `_classify_risk()` - Risk level assignment
- `_find_weak_areas()` - Weak area detection

### AI Advisor
**Responsibilities:**
- Query intent classification
- Context building
- LLM interaction
- Response formatting

**Query Types:**
1. **Intervention** - List high-risk records
2. **Student Risk** - Explain specific record risk
3. **Generate Quiz** - Create personalized quiz
4. **General** - Answer free-form questions

**Key Methods:**
- `handle_query()` - Main entry point
- `_classify_query()` - Intent detection
- `_extract_record_id()` - ID extraction
- `_handle_intervention()` - Intervention handler
- `_handle_student_risk()` - Risk analysis handler
- `_handle_generate_quiz()` - Quiz generator
- `_handle_general()` - General Q&A handler
- `_call_llm()` - Groq API wrapper with retry

## Configuration

### Settings (app/config.py)
```python
GROQ_API_KEY: str           # Groq API key
UPLOAD_DIR: str = "uploads" # Dataset storage
MODELS_DIR: str = "models"  # Model storage
HIGH_RISK_THRESHOLD: float = 0.4   # < 40% = HIGH
LOW_RISK_THRESHOLD: float = 0.65   # < 65% = MEDIUM
```

## Storage Structure

```
project/
├── uploads/
│   ├── dataset1.csv
│   ├── dataset2.csv
│   └── metadata.json          # Dataset metadata
├── models/
│   ├── dataset1.pkl           # Trained RandomForest
│   └── dataset2.pkl
├── app/
│   ├── main.py                # FastAPI app
│   ├── dataset_manager.py     # Dataset management
│   ├── ml_service_dynamic.py  # ML predictions
│   ├── advisor.py             # AI advisor
│   ├── config.py              # Configuration
│   └── schemas.py             # Pydantic models
└── .env                       # Environment variables
```

## Metadata Format

```json
{
  "dataset1": {
    "dataset_path": "uploads/dataset1.csv",
    "column_info": {
      "id_column": "student_id",
      "target_column": "final_result",
      "feature_columns": ["attendance", "marks", ...],
      "topic_columns": ["topic_recursion", ...]
    },
    "model_info": {
      "model_path": "models/dataset1.pkl",
      "accuracy": 0.8523,
      "n_features": 9
    },
    "row_count": 300,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

## Security Considerations

1. **File Upload**: Only CSV files accepted
2. **API Key**: Stored in .env, not in code
3. **Rate Limiting**: Groq API has built-in limits
4. **Input Validation**: Pydantic schemas validate all inputs
5. **Error Handling**: Graceful error messages, no stack traces exposed

## Scalability

**Current Design:**
- In-memory model caching
- File-based storage
- Single-server deployment

**Future Enhancements:**
- Database for metadata (PostgreSQL)
- Object storage for datasets (S3)
- Model versioning
- Async predictions
- Caching layer (Redis)
- Load balancing
- Authentication/Authorization
