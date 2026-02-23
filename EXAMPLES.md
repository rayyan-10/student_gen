# Usage Examples

## Example 1: Student Performance (Original Use Case)

### CSV Structure
```csv
student_id,attendance,internal_marks,assignment_marks,previous_gpa,topic_recursion,topic_sorting,topic_trees,topic_graphs,topic_dp,final_result
1,97,40,91,5.93,89,44,56,85,82,1
2,89,80,83,7.91,36,66,61,66,76,1
3,70,60,51,5.98,60,25,32,42,82,0
```

### Upload
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@students.csv" \
  -F "dataset_id=students_2024"
```

### Response
```json
{
  "success": true,
  "message": "Dataset 'students_2024' uploaded and model trained successfully",
  "details": {
    "dataset_id": "students_2024",
    "rows": 300,
    "columns": {
      "id_column": "student_id",
      "target_column": "final_result",
      "feature_columns": ["attendance", "internal_marks", "assignment_marks", "previous_gpa", "topic_recursion", "topic_sorting", "topic_trees", "topic_graphs", "topic_dp"],
      "topic_columns": ["topic_recursion", "topic_sorting", "topic_trees", "topic_graphs", "topic_dp"]
    },
    "model_accuracy": 0.8523
  }
}
```

### Query Examples
```bash
# Find at-risk students
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which students need intervention?", "dataset_id": "students_2024"}'

# Analyze specific student
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is student 5 at risk?", "dataset_id": "students_2024"}'

# Generate quiz
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Generate quiz for student 10", "dataset_id": "students_2024"}'
```

---

## Example 2: Employee Performance

### CSV Structure
```csv
employee_id,attendance_rate,performance_score,training_hours,years_experience,skill_python,skill_sql,skill_ml,skill_cloud,skill_devops,promotion_eligible
1001,92,85,40,3,88,75,65,70,60,1
1002,78,65,25,2,45,50,40,35,30,0
1003,95,90,50,5,92,88,85,80,75,1
```

### Upload
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@employees.csv" \
  -F "dataset_id=hr_2024"
```

### Auto-Detected Structure
- **ID**: `employee_id`
- **Target**: `promotion_eligible` (0/1)
- **Features**: attendance_rate, performance_score, training_hours, years_experience, skill_python, skill_sql, skill_ml, skill_cloud, skill_devops
- **Topics**: All skill columns (0-100 range)

### Query Examples
```bash
# Find employees needing development
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which employees need intervention?", "dataset_id": "hr_2024"}'

# Analyze specific employee
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is employee 1002 at risk?", "dataset_id": "hr_2024"}'

# Get all predictions
curl "http://localhost:8000/records/hr_2024"
```

---

## Example 3: Patient Health Outcomes

### CSV Structure
```csv
patient_id,age,blood_pressure,cholesterol,bmi,glucose,exercise_hours,sleep_hours,stress_level,healthy
P001,45,120,180,24.5,95,5,7,3,1
P002,62,145,220,28.3,110,2,5,7,0
P003,38,115,170,22.1,88,6,8,2,1
```

### Upload
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@patients.csv" \
  -F "dataset_id=health_study"
```

### Auto-Detected Structure
- **ID**: `patient_id`
- **Target**: `healthy` (0/1)
- **Features**: age, blood_pressure, cholesterol, bmi, glucose, exercise_hours, sleep_hours, stress_level
- **Topics**: blood_pressure, cholesterol, bmi, glucose (0-100 range values)

### Query Examples
```bash
# Find high-risk patients
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which patients need intervention?", "dataset_id": "health_study"}'

# Analyze specific patient
curl "http://localhost:8000/records/health_study/P002"
```

---

## Example 4: Loan Default Prediction

### CSV Structure
```csv
loan_id,income,credit_score,debt_ratio,employment_years,loan_amount,interest_rate,default
L001,75000,720,0.35,5,250000,4.5,0
L002,45000,580,0.65,2,180000,6.2,1
L003,95000,780,0.25,8,320000,3.8,0
```

### Upload
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@loans.csv" \
  -F "dataset_id=loan_risk"
```

### Auto-Detected Structure
- **ID**: `loan_id`
- **Target**: `default` (0/1)
- **Features**: income, credit_score, debt_ratio, employment_years, loan_amount, interest_rate
- **Topics**: credit_score (0-100 range)

### Query Examples
```bash
# Find high-risk loans
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which loans are high risk?", "dataset_id": "loan_risk"}'

# General analysis
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main risk factors?", "dataset_id": "loan_risk"}'
```

---

## Example 5: Customer Churn

### CSV Structure
```csv
customer_id,tenure_months,monthly_charges,total_charges,contract_type,payment_method,support_tickets,satisfaction_score,churned
C001,24,65.50,1572,monthly,auto,2,85,0
C002,6,89.99,539.94,monthly,manual,8,45,1
C003,48,55.20,2649.60,annual,auto,1,92,0
```

### Upload
```bash
curl -X POST "http://localhost:8000/upload_csv" \
  -F "file=@customers.csv" \
  -F "dataset_id=churn_analysis"
```

### Auto-Detected Structure
- **ID**: `customer_id`
- **Target**: `churned` (0/1)
- **Features**: tenure_months, monthly_charges, total_charges, contract_type, payment_method, support_tickets, satisfaction_score
- **Topics**: satisfaction_score (0-100 range)

### Query Examples
```bash
# Find at-risk customers
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which customers are likely to churn?", "dataset_id": "churn_analysis"}'

# Analyze specific customer
curl -X POST "http://localhost:8000/ask_advisor" \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is customer C002 at risk?", "dataset_id": "churn_analysis"}'
```

---

## Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Upload CSV
def upload_dataset(file_path, dataset_id):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'dataset_id': dataset_id}
        response = requests.post(f"{BASE_URL}/upload_csv", files=files, data=data)
        return response.json()

# Ask question
def ask_advisor(query, dataset_id):
    response = requests.post(
        f"{BASE_URL}/ask_advisor",
        json={"query": query, "dataset_id": dataset_id}
    )
    return response.json()

# Get predictions
def get_predictions(dataset_id):
    response = requests.get(f"{BASE_URL}/records/{dataset_id}")
    return response.json()

# Usage
result = upload_dataset("my_data.csv", "my_dataset")
print(f"Uploaded: {result['details']['rows']} rows")
print(f"Accuracy: {result['details']['model_accuracy']}")

answer = ask_advisor("Which records need intervention?", "my_dataset")
print(f"Response: {answer['message']}")

predictions = get_predictions("my_dataset")
print(f"Total records: {predictions['total']}")
high_risk = [r for r in predictions['records'] if r['risk_level'] == 'HIGH']
print(f"High risk: {len(high_risk)}")
```

---

## JavaScript/Node.js Client Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Upload CSV
async function uploadDataset(filePath, datasetId) {
  const form = new FormData();
  form.append('file', fs.createReadStream(filePath));
  form.append('dataset_id', datasetId);
  
  const response = await axios.post(`${BASE_URL}/upload_csv`, form, {
    headers: form.getHeaders()
  });
  return response.data;
}

// Ask question
async function askAdvisor(query, datasetId) {
  const response = await axios.post(`${BASE_URL}/ask_advisor`, {
    query: query,
    dataset_id: datasetId
  });
  return response.data;
}

// Get predictions
async function getPredictions(datasetId) {
  const response = await axios.get(`${BASE_URL}/records/${datasetId}`);
  return response.data;
}

// Usage
(async () => {
  const result = await uploadDataset('my_data.csv', 'my_dataset');
  console.log(`Uploaded: ${result.details.rows} rows`);
  console.log(`Accuracy: ${result.details.model_accuracy}`);
  
  const answer = await askAdvisor('Which records need intervention?', 'my_dataset');
  console.log(`Response: ${answer.message}`);
  
  const predictions = await getPredictions('my_dataset');
  console.log(`Total records: ${predictions.total}`);
  const highRisk = predictions.records.filter(r => r.risk_level === 'HIGH');
  console.log(`High risk: ${highRisk.length}`);
})();
```

---

## Common Query Patterns

### Intervention Queries
- "Which records need intervention?"
- "Show me high-risk cases"
- "Who needs help?"
- "List at-risk records"

### Analysis Queries
- "Why is record 5 at risk?"
- "Analyze record 101"
- "What's wrong with record 42?"
- "Explain the risk for record 7"

### Quiz Generation
- "Generate quiz for record 10"
- "Create practice for record 5"
- "Make quiz for record 15"

### General Queries
- "How many high-risk records are there?"
- "What are the common weak areas?"
- "Show me statistics"
- "What's the overall risk distribution?"

---

## Tips

1. **Column Names**: Use descriptive names, system auto-detects
2. **Target Column**: Must be binary (0/1, yes/no, pass/fail)
3. **Numeric Features**: Better for predictions
4. **Score Columns**: 0-100 range detected as topics
5. **Dataset IDs**: Use descriptive names (students_2024, hr_q1, etc.)
6. **Queries**: Be specific, mention record IDs when needed
