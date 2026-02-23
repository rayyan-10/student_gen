# Demo Guide: Upload → Query Workflow

## Yes, it works exactly as you described! 

Here's the complete workflow:

## 🎯 The Process

```
1. Upload CSV → 2. System Trains Model → 3. Ask Questions → 4. Get AI Answers
```

## 📝 Step-by-Step Example

### Step 1: Start the Server
```bash
uvicorn app.main:app --reload
```

### Step 2: Upload Your CSV

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@students.csv" \
  -F "dataset_id=my_students"
```

**Response:**
```json
{
  "success": true,
  "message": "Dataset 'my_students' uploaded and model trained successfully",
  "details": {
    "dataset_id": "my_students",
    "rows": 300,
    "columns": {
      "id_column": "student_id",
      "target_column": "final_result",
      "feature_columns": ["attendance", "internal_marks", ...],
      "topic_columns": ["topic_recursion", "topic_sorting", ...]
    },
    "model_accuracy": 0.8523
  }
}
```

✅ **Your CSV is now ready to query!**

### Step 3: Ask Questions

**Query 1: Find high-risk records**
```bash
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Which records need intervention?",
    "dataset_id": "my_students"
  }'
```

**Response:**
```json
{
  "response_type": "intervention",
  "message": "Found 45 HIGH-risk students who need immediate intervention:\n\n• Student 5 — Pass Prob: 0.23, Weak Topics: Recursion, Trees\n• Student 12 — Pass Prob: 0.31, Weak Topics: Sorting, Graphs\n...",
  "data": [
    {
      "id": 5,
      "pass_probability": 0.2345,
      "risk_level": "HIGH",
      "weak_areas": ["Recursion", "Trees"],
      "features": {...}
    },
    ...
  ]
}
```

**Query 2: Analyze specific record**
```bash
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Why is student 5 at risk?",
    "dataset_id": "my_students"
  }'
```

**Response:**
```json
{
  "response_type": "student_risk",
  "message": "Student 5 is at high risk due to low attendance (50%) and poor performance in Recursion (25) and Trees (32)",
  "data": {
    "id": 5,
    "pass_probability": 0.2345,
    "risk_level": "HIGH",
    "features": {
      "attendance": 50,
      "internal_marks": 51,
      "assignment_marks": 36,
      ...
    },
    "weak_areas": ["Recursion", "Trees"],
    "ai_analysis": {
      "summary": "Student shows critical deficiencies in core topics",
      "risk_factors": [
        {
          "factor": "Low Attendance",
          "detail": "Only 50% attendance rate",
          "severity": "HIGH"
        },
        ...
      ],
      "recommendations": [
        {
          "action": "Immediate Tutoring",
          "detail": "Focus on Recursion and Trees",
          "priority": 1
        },
        ...
      ]
    }
  }
}
```

**Query 3: Generate quiz**
```bash
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Generate quiz for student 5",
    "dataset_id": "my_students"
  }'
```

**Response:**
```json
{
  "response_type": "generate_quiz",
  "message": "Generated Easy-level quiz for Student 5 targeting weak topics: Recursion, Trees",
  "data": {
    "target_id": 5,
    "risk_level": "HIGH",
    "weakest_areas": ["Recursion", "Trees"],
    "mcqs": [
      {
        "question": "What is the base case in recursion?",
        "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "correct_answer": "A",
        "difficulty": "Easy"
      },
      ...
    ],
    "coding_problem": "Write a recursive function to...",
    "conceptual_explanation": "Recursion is a technique where..."
  }
}
```

## 🎬 Run the Demo

I've created a demo script that shows the complete workflow:

```bash
# Make sure server is running
uvicorn app.main:app --reload

# In another terminal, run the demo
python demo_simple.py
```

This will:
1. ✅ Upload students.csv
2. ✅ Ask "Which records need intervention?"
3. ✅ Analyze specific record (ID 5)
4. ✅ Ask "Why is student 5 at risk?"

## 🔄 The Complete Flow

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR CSV FILE                        │
│  (any structure, any domain, any column names)          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              POST /upload_csv                           │
│  • Auto-detects columns                                 │
│  • Trains RandomForest model                            │
│  • Saves dataset and model                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         Dataset Ready for Queries! ✅                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              POST /ask_advisor                          │
│  • Loads your dataset                                   │
│  • Runs predictions                                     │
│  • AI analyzes results                                  │
│  • Returns intelligent answer                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              YOU GET THE ANSWER! 🎉                     │
└─────────────────────────────────────────────────────────┘
```

## ✅ Confirmation

**Q: "I upload a CSV file and ask query based on that, will it give the output?"**

**A: YES! Absolutely!**

1. Upload your CSV → System trains model automatically
2. Ask any question → System uses YOUR data to answer
3. Get AI-powered insights → Based on YOUR uploaded CSV

## 🧪 Test It Yourself

### Quick Test (30 seconds)

```bash
# Terminal 1: Start server
uvicorn app.main:app --reload

# Terminal 2: Upload and query
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@students.csv" \
  -F "dataset_id=test"

curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which records need help?", "dataset_id": "test"}'
```

You'll get an immediate response based on your uploaded data!

## 💡 Key Points

1. **Upload Once** - Model trains automatically
2. **Query Many Times** - Ask as many questions as you want
3. **Multiple Datasets** - Upload different CSVs with different IDs
4. **Instant Results** - No manual training needed
5. **AI-Powered** - Groq LLaMA generates intelligent responses

## 🎯 Example Queries You Can Ask

After uploading your CSV:

- "Which records need intervention?"
- "Why is record 5 at risk?"
- "Generate quiz for record 10"
- "How many high-risk records are there?"
- "What are the common weak areas?"
- "Show me the top 5 at-risk records"
- "What's the overall risk distribution?"
- "Which features are most important?"

All answers will be based on YOUR uploaded CSV data!

## 🚀 Try It Now!

```bash
# 1. Start server
uvicorn app.main:app --reload

# 2. Run demo
python demo_simple.py

# 3. See it work! ✨
```
