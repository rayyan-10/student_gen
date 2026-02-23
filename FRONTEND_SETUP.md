# Frontend Setup Guide

## The Issue

Your frontend shows: **"Dataset 'default' not found"**

This happens because:
1. Frontend sends queries with `dataset_id: "default"`
2. But no dataset with ID "default" has been uploaded yet
3. Backend returns 200 OK (request was valid) but with an error message

## The Solution

### Quick Fix (30 seconds)

Run this script to upload students.csv as the default dataset:

```bash
python setup_default_dataset.py
```

This will:
- ✅ Upload students.csv with ID "default"
- ✅ Train the model automatically
- ✅ Test the AI advisor
- ✅ Make your frontend work immediately

### Manual Fix

```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@students.csv" \
  -F "dataset_id=default"
```

### Verify It Works

```bash
# Check available datasets
curl http://localhost:8000/datasets

# Test the advisor
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which students need intervention?", "dataset_id": "default"}'
```

## Why This Happened

### Backend Code (Correct)
```python
class AdvisorRequest(BaseModel):
    query: str
    dataset_id: Optional[str] = "default"  # Defaults to "default"
```

The backend expects a dataset with ID "default" to exist, but it wasn't uploaded yet.

### Frontend Code (Correct)
Your frontend is correctly sending requests, but the "default" dataset doesn't exist yet.

## Better Error Handling

I've updated the backend to provide clearer error messages:

**Before:**
```
ValueError: Dataset 'default' not found
```

**After:**
```json
{
  "response_type": "error",
  "message": "Dataset 'default' not found. Available datasets: students_2024, hr_data. Please upload a dataset with ID 'default' or use one of the available datasets.",
  "data": {
    "available_datasets": ["students_2024", "hr_data"]
  }
}
```

## Frontend Integration Tips

### Option 1: Use "default" dataset (Recommended)
Always have a dataset with ID "default" uploaded:

```bash
python setup_default_dataset.py
```

### Option 2: Let users select dataset
Update your frontend to:
1. Fetch available datasets: `GET /datasets`
2. Let user select which dataset to query
3. Send selected `dataset_id` in requests

### Option 3: Dynamic dataset selection
```javascript
// Fetch available datasets
const response = await fetch('http://localhost:8000/datasets');
const data = await response.json();
const datasets = data.datasets;

// Use first available dataset or "default"
const datasetId = datasets.length > 0 ? datasets[0].dataset_id : "default";

// Send query
await fetch('http://localhost:8000/ask_advisor', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: userQuery,
    dataset_id: datasetId
  })
});
```

## Health Check Endpoint

I've added a health check endpoint to help debug:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "datasets_count": 1,
  "datasets": ["default"]
}
```

## Complete Workflow

### 1. Start Backend
```bash
uvicorn app.main:app --reload
```

### 2. Setup Default Dataset
```bash
python setup_default_dataset.py
```

### 3. Start Frontend
```bash
# Your frontend command
npm run dev
# or
yarn dev
```

### 4. Use the Application
- Frontend will now work with the "default" dataset
- All queries will return proper results

## Troubleshooting

### "students.csv not found"
Make sure you're in the project root directory where students.csv exists.

### "Server not responding"
Start the backend first:
```bash
uvicorn app.main:app --reload
```

### "Still showing error"
Check which datasets are available:
```bash
curl http://localhost:8000/datasets
```

If "default" is not in the list, run:
```bash
python setup_default_dataset.py
```

## API Endpoints Summary

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Check system status and available datasets |
| `GET /datasets` | List all uploaded datasets |
| `POST /upload_csv` | Upload a new dataset |
| `POST /ask_advisor` | Ask questions (requires dataset_id) |
| `GET /records/{dataset_id}` | Get all predictions |

## Example Frontend Code

### Check if default dataset exists
```javascript
async function ensureDefaultDataset() {
  const response = await fetch('http://localhost:8000/health');
  const data = await response.json();
  
  if (!data.datasets.includes('default')) {
    alert('Please upload a dataset with ID "default" first');
    return false;
  }
  return true;
}
```

### Send query with error handling
```javascript
async function askAdvisor(query) {
  try {
    const response = await fetch('http://localhost:8000/ask_advisor', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query,
        dataset_id: 'default'
      })
    });
    
    const data = await response.json();
    
    if (data.response_type === 'error') {
      console.error('Error:', data.message);
      alert(data.message);
      return null;
    }
    
    return data;
  } catch (error) {
    console.error('Request failed:', error);
    alert('Failed to connect to backend');
    return null;
  }
}
```

## Summary

**Problem:** Frontend expects "default" dataset but it doesn't exist
**Solution:** Run `python setup_default_dataset.py`
**Result:** Frontend works immediately! ✅

No backend code errors - just need to upload the default dataset!
