"""
Simple demo showing upload → query workflow
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("DEMO: Upload CSV and Query")
print("=" * 70)

# Step 1: Upload the students.csv file
print("\n📤 STEP 1: Uploading students.csv...")
print("-" * 70)

with open("students.csv", "rb") as f:
    files = {"file": ("students.csv", f, "text/csv")}
    data = {"dataset_id": "demo_dataset"}
    
    response = requests.post(f"{BASE_URL}/upload_csv", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Upload successful!")
        print(f"   Dataset ID: {result['details']['dataset_id']}")
        print(f"   Rows: {result['details']['rows']}")
        print(f"   Model Accuracy: {result['details']['model_accuracy']}")
        print(f"   Detected Columns:")
        print(f"      - ID: {result['details']['columns']['id_column']}")
        print(f"      - Target: {result['details']['columns']['target_column']}")
        print(f"      - Features: {len(result['details']['columns']['feature_columns'])}")
    else:
        print(f"❌ Upload failed: {response.text}")
        exit(1)

# Wait a moment
time.sleep(1)

# Step 2: Ask a question
print("\n💬 STEP 2: Asking 'Which records need intervention?'")
print("-" * 70)

query_data = {
    "query": "Which records need intervention?",
    "dataset_id": "demo_dataset"
}

response = requests.post(
    f"{BASE_URL}/ask_advisor",
    json=query_data
)

if response.status_code == 200:
    result = response.json()
    print("✅ Query successful!")
    print(f"   Response Type: {result['response_type']}")
    print(f"\n   AI Response:")
    print(f"   {result['message'][:500]}...")
    
    if result['data']:
        high_risk_count = len(result['data'])
        print(f"\n   📊 Found {high_risk_count} high-risk records")
        
        # Show first 3
        print("\n   First 3 high-risk records:")
        for record in result['data'][:3]:
            print(f"      • ID {record['id']}: {record['pass_probability']:.2%} pass probability")
            print(f"        Weak areas: {', '.join(record['weak_areas']) if record['weak_areas'] else 'None'}")
else:
    print(f"❌ Query failed: {response.text}")
    exit(1)

# Step 3: Get specific record analysis
print("\n🔍 STEP 3: Analyzing specific record (ID 5)")
print("-" * 70)

response = requests.get(f"{BASE_URL}/records/demo_dataset/5")

if response.status_code == 200:
    result = response.json()
    print("✅ Analysis successful!")
    print(f"   ID: {result['id']}")
    print(f"   Pass Probability: {result['pass_probability']:.2%}")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Weak Areas: {', '.join(result['weak_areas']) if result['weak_areas'] else 'None'}")
    print(f"\n   Features:")
    for key, value in list(result['features'].items())[:5]:
        print(f"      - {key}: {value}")
else:
    print(f"❌ Analysis failed: {response.text}")

# Step 4: Ask another question
print("\n💬 STEP 4: Asking 'Why is student 5 at risk?'")
print("-" * 70)

query_data = {
    "query": "Why is student 5 at risk?",
    "dataset_id": "demo_dataset"
}

response = requests.post(
    f"{BASE_URL}/ask_advisor",
    json=query_data
)

if response.status_code == 200:
    result = response.json()
    print("✅ Query successful!")
    print(f"   Response Type: {result['response_type']}")
    print(f"\n   AI Analysis:")
    print(f"   {result['message']}")
else:
    print(f"❌ Query failed: {response.text}")

print("\n" + "=" * 70)
print("✅ DEMO COMPLETE!")
print("=" * 70)
print("\nYou can now:")
print("1. Upload your own CSV files")
print("2. Ask any questions about the data")
print("3. Get AI-powered insights")
print("\nTry it yourself:")
print("  curl -X POST 'http://localhost:8000/upload_csv' \\")
print("    -F 'file=@your_file.csv' \\")
print("    -F 'dataset_id=my_data'")
