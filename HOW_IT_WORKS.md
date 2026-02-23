# How It Works: Upload → Query → Answer

## ✅ YES! It works exactly as you described!

You upload a CSV → Ask questions → Get AI-powered answers based on YOUR data.

---

## 🎬 Visual Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  STEP 1: You Upload Your CSV                                │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  POST /upload_csv                                            │
│  file: your_data.csv                                         │
│  dataset_id: "my_dataset"                                    │
│                                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  SYSTEM AUTOMATICALLY:                                       │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  ✓ Detects columns (ID, features, target)                   │
│  ✓ Trains RandomForest model                                │
│  ✓ Saves dataset to uploads/my_dataset.csv                  │
│  ✓ Saves model to models/my_dataset.pkl                     │
│  ✓ Stores metadata                                          │
│                                                              │
│  Returns: "Success! Model accuracy: 85.23%"                 │
│                                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  STEP 2: You Ask Questions                                  │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  POST /ask_advisor                                           │
│  query: "Which records need intervention?"                   │
│  dataset_id: "my_dataset"                                    │
│                                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  SYSTEM AUTOMATICALLY:                                       │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  ✓ Loads YOUR dataset (my_dataset.csv)                      │
│  ✓ Loads YOUR model (my_dataset.pkl)                        │
│  ✓ Runs predictions on YOUR data                            │
│  ✓ Identifies high-risk records                             │
│  ✓ Sends context to Groq AI                                 │
│  ✓ AI generates intelligent response                        │
│                                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│  STEP 3: You Get AI-Powered Answer                          │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  Response:                                                   │
│  "Found 45 HIGH-risk records that need intervention:        │
│   • Record 5 — Pass Prob: 23%, Weak: Recursion, Trees       │
│   • Record 12 — Pass Prob: 31%, Weak: Sorting, Graphs       │
│   ..."                                                       │
│                                                              │
│  Data: [detailed list of all high-risk records]             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔄 The Complete Cycle

### Upload Phase (Once)
```
Your CSV File
     ↓
Upload API
     ↓
Auto-detect columns
     ↓
Train model
     ↓
Save everything
     ↓
✅ Ready to query!
```

### Query Phase (Many times)
```
Your Question
     ↓
Load YOUR dataset
     ↓
Load YOUR model
     ↓
Run predictions
     ↓
AI analyzes
     ↓
✅ Get answer!
```

---

## 💡 Real Example

### You Upload:
```csv
student_id,attendance,marks,passed
1,85,75,1
2,60,45,0
3,90,88,1
4,55,40,0
5,50,35,0
```

### System Trains:
```
✓ Detected: student_id (ID), passed (target)
✓ Features: attendance, marks
✓ Model trained: 80% accuracy
✓ Ready for queries!
```

### You Ask:
```
"Which students need intervention?"
```

### System Responds:
```json
{
  "message": "Found 2 HIGH-risk students:
              • Student 4: 35% pass probability
              • Student 5: 28% pass probability",
  "data": [
    {
      "id": 4,
      "pass_probability": 0.35,
      "risk_level": "HIGH",
      "features": {"attendance": 55, "marks": 40}
    },
    {
      "id": 5,
      "pass_probability": 0.28,
      "risk_level": "HIGH",
      "features": {"attendance": 50, "marks": 35}
    }
  ]
}
```

---

## 🎯 Key Points

### ✅ What Happens Automatically:
1. **Column Detection** - System figures out your CSV structure
2. **Model Training** - RandomForest trains on your data
3. **Predictions** - Model predicts outcomes for all records
4. **AI Analysis** - Groq LLaMA generates insights
5. **Structured Response** - You get JSON with data + explanation

### ✅ What You Need to Do:
1. **Upload CSV** - One API call
2. **Ask Questions** - As many as you want
3. **Get Answers** - Instant responses

### ✅ What You DON'T Need to Do:
- ❌ Write code
- ❌ Train models manually
- ❌ Configure columns
- ❌ Process data
- ❌ Format responses

---

## 🧪 Try It Right Now

### Terminal 1: Start Server
```bash
uvicorn app.main:app --reload
```

### Terminal 2: Upload & Query
```bash
# Upload
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@students.csv" \
  -F "dataset_id=test"

# Query
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which records need help?", "dataset_id": "test"}'
```

### Result:
You'll get an immediate AI-powered response based on your uploaded CSV! 🎉

---

## 📊 Data Flow Diagram

```
┌─────────────┐
│  Your CSV   │
└──────┬──────┘
       │
       │ Upload
       ▼
┌─────────────────────┐
│  Dataset Manager    │
│  • Detect columns   │
│  • Train model      │
│  • Save files       │
└──────┬──────────────┘
       │
       │ Ready
       ▼
┌─────────────────────┐
│  Your Question      │
└──────┬──────────────┘
       │
       │ Query
       ▼
┌─────────────────────┐
│  ML Service         │
│  • Load dataset     │
│  • Run predictions  │
│  • Classify risk    │
└──────┬──────────────┘
       │
       │ Results
       ▼
┌─────────────────────┐
│  AI Advisor         │
│  • Analyze data     │
│  • Generate insight │
│  • Format response  │
└──────┬──────────────┘
       │
       │ Answer
       ▼
┌─────────────────────┐
│  Your Answer! ✅    │
└─────────────────────┘
```

---

## ✨ The Magic

**You:** Upload CSV + Ask question
**System:** Automatically trains, predicts, analyzes, and responds
**You:** Get intelligent answer based on YOUR data

No manual work. No configuration. Just upload and query! 🚀

---

## 🎬 Watch It Work

Run the demo:
```bash
python demo_simple.py
```

This will show you the complete workflow in action!

---

## ❓ Your Question Answered

**Q: "I upload a CSV file and ask query based on that, will it give the output?"**

**A: YES! 100% YES!**

1. ✅ Upload your CSV → System trains automatically
2. ✅ Ask your question → System uses YOUR data
3. ✅ Get AI answer → Based on YOUR uploaded CSV

**It's that simple!** 🎉
