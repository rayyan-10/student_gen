# Troubleshooting Guide

## Common Issues and Solutions

### 1. Server Won't Start

#### Error: "Address already in use"
```
ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)
```

**Solution:**
```bash
# Windows - Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <process_id> /F

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

#### Error: "ModuleNotFoundError: No module named 'app'"
```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
```bash
# Make sure you're in the project root directory
cd /path/to/project

# Verify app/ folder exists
ls app/

# Run from project root
uvicorn app.main:app --reload
```

---

### 2. CSV Upload Issues

#### Error: "Could not detect a binary target column"
```
ValueError: Could not detect a binary target column
```

**Cause:** Your CSV doesn't have a column with exactly 2 unique values.

**Solution:**
```python
# Check your CSV
import pandas as pd
df = pd.read_csv("your_file.csv")

# Check unique values in each column
for col in df.columns:
    print(f"{col}: {df[col].nunique()} unique values")

# Your target column should have exactly 2 unique values
# Examples: 0/1, yes/no, pass/fail, true/false
```

**Fix your CSV:**
```csv
# BAD - 3 values (0, 1, 2)
id,score,result
1,85,2
2,45,0
3,75,1

# GOOD - 2 values (0, 1)
id,score,result
1,85,1
2,45,0
3,75,1
```

#### Error: "Only CSV files are supported"
```
HTTPException: Only CSV files are supported
```

**Solution:**
- Make sure your file has `.csv` extension
- Convert Excel files to CSV first
- Use proper CSV format (comma-separated)

---

### 3. API Request Issues

#### Error: "Dataset 'xyz' not found"
```
ValueError: Dataset 'xyz' not found
```

**Solution:**
```bash
# List all available datasets
curl http://localhost:8000/datasets

# Use the correct dataset_id from the list
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "...", "dataset_id": "correct_id"}'
```

#### Error: "Record X not found"
```
Record 999 not found in dataset 'my_dataset'
```

**Solution:**
```bash
# Check available records
curl http://localhost:8000/records/my_dataset

# Use a valid record ID from the response
```

---

### 4. Groq API Issues

#### Error: "Rate limit exceeded"
```
RuntimeError: Groq API rate limit exceeded after retries
```

**Solution:**
- Wait 60 seconds before trying again
- Groq free tier has rate limits
- Consider upgrading your Groq plan
- Reduce query frequency

#### Error: "Invalid API key"
```
AuthenticationError: Invalid API key
```

**Solution:**
```bash
# Check your .env file
cat .env

# Should contain:
GROQ_API_KEY=gsk_your_actual_key_here

# Get a new key from: https://console.groq.com/keys

# Restart the server after updating .env
```

---

### 5. Prediction Issues

#### Error: "Model accuracy is very low"
```
model_accuracy: 0.45
```

**Possible Causes:**
1. Not enough data (< 100 rows)
2. Features don't correlate with target
3. Imbalanced dataset (95% one class)
4. Random/noisy data

**Solutions:**
```python
# Check dataset size
import pandas as pd
df = pd.read_csv("your_file.csv")
print(f"Rows: {len(df)}")  # Should be > 100

# Check class balance
print(df['target_column'].value_counts())
# Should be somewhat balanced (not 95% vs 5%)

# Check feature correlation
print(df.corr())
# Features should correlate with target
```

#### Error: "All records classified as same risk level"
```
All records: HIGH risk
```

**Cause:** Model predictions are all similar.

**Solution:**
- Check if your data has enough variance
- Ensure features are meaningful
- Try with more diverse data

---

### 6. Installation Issues

#### Error: "pip install fails"
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solution:**
```bash
# Update pip
python -m pip install --upgrade pip

# Install one by one to identify the problem
pip install fastapi
pip install uvicorn[standard]
pip install pandas
pip install scikit-learn
pip install joblib
pip install python-dotenv
pip install pydantic-settings
pip install groq
pip install python-multipart
```

#### Error: "Python version incompatible"
```
ERROR: Package requires Python >=3.8
```

**Solution:**
```bash
# Check Python version
python --version

# Should be 3.8 or higher
# If not, install Python 3.8+
```

---

### 7. File Permission Issues

#### Error: "Permission denied" when creating uploads/
```
PermissionError: [Errno 13] Permission denied: 'uploads'
```

**Solution:**
```bash
# Windows
mkdir uploads
mkdir models

# Or run as administrator
```

---

### 8. JSON Parsing Issues

#### Error: "Expecting value: line 1 column 1"
```
json.JSONDecodeError: Expecting value: line 1 column 1
```

**Cause:** LLM returned non-JSON response.

**Solution:**
- This is handled automatically with retry logic
- If persistent, check Groq API status
- Try a different query

---

### 9. Memory Issues

#### Error: "MemoryError" with large CSV
```
MemoryError: Unable to allocate array
```

**Solution:**
```python
# For very large files (> 1GB), consider:
# 1. Sample your data
import pandas as pd
df = pd.read_csv("large_file.csv")
df_sample = df.sample(n=10000)  # Use 10k rows
df_sample.to_csv("sample.csv", index=False)

# 2. Or increase system memory
# 3. Or use chunking (requires code modification)
```

---

### 10. CORS Issues (Frontend Integration)

#### Error: "CORS policy blocked"
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solution:**
Already configured! CORS is enabled for all origins in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Already set
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If still having issues:
```python
# Restrict to specific origin
allow_origins=["http://localhost:3000"]
```

---

## Debugging Tips

### 1. Enable Verbose Logging
```python
# Add to app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Check Server Logs
```bash
# Server logs show all requests and errors
uvicorn app.main:app --reload --log-level debug
```

### 3. Test with cURL First
```bash
# Before using frontend, test with cURL
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@test.csv" \
  -F "dataset_id=test"
```

### 4. Validate CSV Structure
```python
import pandas as pd

df = pd.read_csv("your_file.csv")
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)
print("Dtypes:", df.dtypes)
print("Null values:", df.isnull().sum())
print("Unique values per column:")
for col in df.columns:
    print(f"  {col}: {df[col].nunique()}")
```

### 5. Check API Response
```bash
# Get detailed error messages
curl -v http://localhost:8000/datasets
```

---

## Getting Help

### 1. Check Documentation
- `README.md` - Full documentation
- `QUICKSTART.md` - Setup guide
- `EXAMPLES.md` - Usage examples
- `ARCHITECTURE.md` - System design

### 2. Check API Docs
Visit: http://localhost:8000/docs

### 3. Verify Installation
```bash
# Check all dependencies
pip list | grep -E "fastapi|uvicorn|pandas|scikit|groq|multipart"

# Should show:
# fastapi
# uvicorn
# pandas
# scikit-learn
# groq
# python-multipart
```

### 4. Test with Example Data
```bash
# Use provided example
python test_upload.py

# Should complete without errors
```

---

## Quick Diagnostic Checklist

```
□ Python 3.8+ installed
□ All dependencies installed (pip install -r requirements.txt)
□ .env file exists with valid GROQ_API_KEY
□ Running from project root directory
□ Port 8000 is available
□ CSV file has binary target column
□ CSV file is properly formatted
□ Server starts without errors
□ Can access http://localhost:8000
□ Can access http://localhost:8000/docs
```

---

## Still Having Issues?

1. **Check the logs** - Server output shows detailed errors
2. **Try the test script** - `python test_upload.py`
3. **Verify CSV format** - Use pandas to inspect
4. **Test with example** - Use `students.csv` or `example_custom.csv`
5. **Restart server** - Sometimes a fresh start helps
6. **Check Groq API** - Verify your API key is valid

---

## Common Mistakes

### ❌ Wrong: Running from wrong directory
```bash
cd app/
uvicorn main:app --reload  # Won't work!
```

### ✅ Right: Run from project root
```bash
cd project_root/
uvicorn app.main:app --reload  # Works!
```

### ❌ Wrong: Missing dataset_id
```json
{"query": "Which records need help?"}
```

### ✅ Right: Include dataset_id
```json
{"query": "Which records need help?", "dataset_id": "my_dataset"}
```

### ❌ Wrong: Non-binary target
```csv
id,score,grade
1,85,A
2,75,B
3,65,C
```

### ✅ Right: Binary target
```csv
id,score,passed
1,85,1
2,75,1
3,65,0
```
