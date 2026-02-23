# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Edit `.env` file and add your Groq API key:
```
GROQ_API_KEY=your_actual_key_here
```

### 3. Start the Server
```bash
uvicorn app.main:app --reload
```

Server will run at: `http://localhost:8000`

## Test with Existing Data

### Option 1: Use the Test Script
```bash
python test_upload.py
```

This will:
- Upload the students.csv file
- List all datasets
- Ask the AI advisor questions
- Get predictions for all records

### Option 2: Manual Testing with cURL

#### Upload a CSV
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@students.csv" \
  -F "dataset_id=my_students"
```

#### Ask a Question
```bash
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which records need intervention?", "dataset_id": "my_students"}'
```

#### Get All Predictions
```bash
curl "http://localhost:8000/records/my_students"
```

#### Get Specific Record
```bash
curl "http://localhost:8000/records/my_students/5"
```

## Try with Your Own CSV

Your CSV just needs:
1. **An ID column** (optional) - first column or contains "id"
2. **Feature columns** - any numeric or categorical data
3. **A binary target column** - must have exactly 2 values (0/1, pass/fail, etc.)

Example CSV structure:
```csv
id,feature1,feature2,feature3,outcome
1,85,90,75,1
2,45,50,40,0
3,92,88,95,1
```

Upload it:
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@your_data.csv" \
  -F "dataset_id=my_dataset"
```

## Example Queries

Once uploaded, ask questions like:

- "Which records need intervention?"
- "Why is record 5 at risk?"
- "Generate quiz for record 10"
- "How many high-risk records are there?"
- "What are the common weak areas?"
- "Show me the top 5 at-risk records"

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## What Happens Behind the Scenes

1. **Upload**: System detects columns, trains RandomForest model
2. **Prediction**: Model predicts pass probability for each record
3. **Risk Classification**: 
   - HIGH: < 40% pass probability
   - MEDIUM: 40-65% pass probability
   - LOW: > 65% pass probability
4. **Weak Area Detection**: Identifies features with scores < 50
5. **AI Analysis**: Groq LLaMA generates insights and recommendations

## Troubleshooting

### "Dataset not found"
Make sure you uploaded the CSV first and use the correct dataset_id.

### "Could not detect binary target column"
Your CSV needs a column with exactly 2 unique values (like 0/1 or pass/fail).

### "Rate limit exceeded"
The Groq API has rate limits. Wait a minute and try again.

### Server won't start
Check that port 8000 is not already in use:
```bash
# Windows
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /PID <process_id> /F
```

## Next Steps

- Check out `README.md` for detailed documentation
- Explore the API at `http://localhost:8000/docs`
- Try the example custom CSV: `example_custom.csv`
- Modify risk thresholds in `app/config.py`
