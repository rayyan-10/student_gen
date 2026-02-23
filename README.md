# Dynamic Student Result Analysis — GenAI Academic Advisor

A flexible AI-powered system that works with **any CSV dataset** to predict outcomes and provide intelligent insights.

## Key Features

- **Upload Any CSV**: Automatically detects columns and trains a model
- **Dynamic Column Detection**: Works with different feature names and structures
- **AI-Powered Insights**: Uses Groq LLaMA for intelligent analysis
- **Risk Classification**: Automatically identifies high-risk records
- **Personalized Quizzes**: Generates targeted interventions
- **Multi-Dataset Support**: Manage multiple datasets simultaneously

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Upload a CSV Dataset

```bash
POST /upload_csv
```

Upload any CSV file with:
- An ID column (optional, auto-detected)
- Feature columns (numeric or categorical)
- A binary target column (0/1 for fail/pass)

Example:
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@your_data.csv" \
  -F "dataset_id=my_dataset"
```

### List All Datasets

```bash
GET /datasets
```

### Ask the AI Advisor

```bash
POST /ask_advisor
{
  "query": "Which records need intervention?",
  "dataset_id": "my_dataset"
}
```

Supported queries:
- "Which records need intervention?"
- "Why is record 101 at risk?"
- "Generate quiz for record 101"
- Any general question about the data

### Get All Records with Predictions

```bash
GET /records/{dataset_id}
```

### Get Specific Record Analysis

```bash
GET /records/{dataset_id}/{record_id}
```

### Delete a Dataset

```bash
DELETE /datasets/{dataset_id}
```

## How It Works

### 1. Automatic Column Detection

When you upload a CSV, the system automatically:
- Detects the ID column (first column or contains "id")
- Identifies the binary target column (contains "result", "pass", "fail", etc.)
- Extracts all feature columns
- Identifies numeric score columns for weak area analysis

### 2. Model Training

- Trains a RandomForest classifier on your data
- Evaluates accuracy on test set
- Saves the model for future predictions

### 3. Risk Analysis

- Classifies records as HIGH (<40%), MEDIUM (40-65%), or LOW (>65%) risk
- Identifies weak areas (scores below 50)
- Provides AI-generated recommendations

### 4. AI-Powered Insights

Uses Groq's LLaMA model to:
- Explain risk factors
- Generate personalized quizzes
- Answer questions about the data
- Provide actionable recommendations

## Example CSV Structure

Your CSV can have any column names. Here's an example:

```csv
student_id,attendance,quiz_score,homework,gpa,final_result
1,85,75,80,3.5,1
2,60,45,50,2.1,0
3,90,88,92,3.8,1
```

The system will automatically detect:
- `student_id` as the ID column
- `final_result` as the target (0=fail, 1=pass)
- `attendance`, `quiz_score`, `homework`, `gpa` as features
- Numeric features as potential weak areas

## Configuration

Edit `app/config.py` to adjust:
- `HIGH_RISK_THRESHOLD`: Default 0.4 (40%)
- `LOW_RISK_THRESHOLD`: Default 0.65 (65%)
- `UPLOAD_DIR`: Where datasets are stored
- `MODELS_DIR`: Where trained models are saved

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Architecture

- `app/main.py` - FastAPI application with all endpoints
- `app/dataset_manager.py` - Manages multiple datasets and models
- `app/ml_service_dynamic.py` - Dynamic ML predictions
- `app/advisor.py` - AI-powered query handling
- `app/config.py` - Configuration settings
- `app/schemas.py` - Pydantic models

## License

MIT
