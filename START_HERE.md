# 🚀 START HERE

## Welcome to the Dynamic CSV Analysis System!

This system can work with **ANY CSV file** to predict outcomes and provide AI-powered insights.

## ✅ YES! Upload CSV → Ask Questions → Get AI Answers

**Your Question:** "I upload a CSV file and ask query based on that, will it give the output?"

**Answer:** **YES! Absolutely!** 

1. Upload your CSV → System trains model automatically
2. Ask any question → System analyzes YOUR data
3. Get AI-powered answer → Based on YOUR uploaded CSV

See [HOW_IT_WORKS.md](HOW_IT_WORKS.md) for detailed explanation or [DEMO_GUIDE.md](DEMO_GUIDE.md) for examples.

---

## ⚡ Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Your API Key
Edit `.env` file:
```
GROQ_API_KEY=your_key_here
```
Get a free key at: https://console.groq.com/keys

### 3. Start the Server
```bash
uvicorn app.main:app --reload
```

### 4. Upload Your CSV
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@your_data.csv" \
  -F "dataset_id=my_dataset"
```

### 5. Ask Questions
```bash
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which records need intervention?", "dataset_id": "my_dataset"}'
```

---

## 📖 Documentation Guide

### New User?
1. Read this file (you're here!)
2. Follow the Quick Start above
3. Check [EXAMPLES.md](EXAMPLES.md) for more examples
4. Visit http://localhost:8000/docs for API docs

### Want to Understand the System?
- [SUMMARY.md](SUMMARY.md) - What was built
- [VISUAL_GUIDE.md](VISUAL_GUIDE.md) - Visual comparison
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details

### Need Help?
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [QUICKSTART.md](QUICKSTART.md) - Detailed setup
- [INDEX.md](INDEX.md) - Full documentation index

---

## ✨ What Makes This Special?

### Before (v1.0)
- ❌ Only worked with students.csv
- ❌ Hardcoded column names
- ❌ Single dataset only

### After (v2.0)
- ✅ Works with ANY CSV
- ✅ Auto-detects columns
- ✅ Multiple datasets
- ✅ Upload via API

---

## 🎯 What Can You Do?

### Upload Any CSV
```csv
id,feature1,feature2,target
1,85,90,1
2,45,50,0
```

### Get Predictions
- Risk classification (HIGH/MEDIUM/LOW)
- Weak area identification
- Pass probability scores

### Ask AI Questions
- "Which records need intervention?"
- "Why is record 5 at risk?"
- "Generate quiz for record 10"
- "Show me statistics"

---

## 📊 Supported Use Cases

- 📚 **Education**: Student performance prediction
- 👔 **HR**: Employee promotion prediction
- 🏥 **Healthcare**: Patient outcome prediction
- 💰 **Finance**: Loan default prediction
- 🛒 **E-commerce**: Customer churn prediction
- ✨ **Any binary classification problem!**

---

## 🔧 Requirements

### Your CSV Must Have:
1. **Features** - Any columns with data
2. **Binary Target** - Exactly 2 values (0/1, yes/no, pass/fail)
3. **Optional ID** - First column or contains "id"

### Example:
```csv
student_id,attendance,test_score,passed
1,85,75,1
2,60,45,0
```

---

## 🎓 Learning Path

### Beginner (30 min)
1. Follow Quick Start above
2. Upload students.csv
3. Try example queries
4. Explore API docs

### Intermediate (2 hours)
1. Read [EXAMPLES.md](EXAMPLES.md)
2. Try different CSV files
3. Explore all endpoints
4. Read [README.md](README.md)

### Advanced (4 hours)
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Study the code
3. Customize features
4. Deploy to production

---

## 🚨 Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

### "Could not detect target column"
Your CSV needs a column with exactly 2 unique values.

### More help?
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📚 Full Documentation

- [INDEX.md](INDEX.md) - Documentation index
- [README.md](README.md) - Complete documentation
- [QUICKSTART.md](QUICKSTART.md) - Detailed setup
- [EXAMPLES.md](EXAMPLES.md) - Usage examples
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solving

---

## 🎉 Ready to Start?

```bash
# 1. Install
pip install -r requirements.txt

# 2. Start server
uvicorn app.main:app --reload

# 3. Visit
http://localhost:8000/docs

# 4. Upload your CSV and start querying!
```

---

## 💡 Pro Tips

1. **Test with example first**: Use `students.csv` or `example_custom.csv`
2. **Check API docs**: Visit http://localhost:8000/docs
3. **Use descriptive dataset IDs**: `students_2024` not `dataset1`
4. **Validate CSV first**: Check it has binary target column
5. **Read examples**: See [EXAMPLES.md](EXAMPLES.md) for patterns

---

## 🤝 Need Help?

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [EXAMPLES.md](EXAMPLES.md)
3. Test with `python test_upload.py`
4. Check server logs for errors

---

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] API key in .env
- [ ] Server starts successfully
- [ ] Can access http://localhost:8000
- [ ] Can access http://localhost:8000/docs
- [ ] Uploaded first CSV
- [ ] Got predictions
- [ ] Asked AI advisor

---

**All set? Start with the Quick Start above! 🚀**

**Questions? Check [INDEX.md](INDEX.md) for full documentation.**
