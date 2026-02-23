"""
Setup script to upload students.csv as the default dataset.
Run this after starting the server to make the frontend work immediately.
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("Setting up default dataset for frontend")
print("=" * 70)

# Check if server is running
try:
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print("❌ Server is not responding. Please start it first:")
        print("   uvicorn app.main:app --reload")
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to server. Please start it first:")
    print("   uvicorn app.main:app --reload")
    sys.exit(1)

print("✓ Server is running")

# Upload students.csv as default dataset
print("\n📤 Uploading students.csv as 'default' dataset...")

try:
    with open("students.csv", "rb") as f:
        files = {"file": ("students.csv", f, "text/csv")}
        data = {"dataset_id": "default"}
        
        response = requests.post(f"{BASE_URL}/upload_csv", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print(f"   Dataset ID: default")
            print(f"   Rows: {result['details']['rows']}")
            print(f"   Model Accuracy: {result['details']['model_accuracy']}")
            print(f"   Columns detected:")
            print(f"      - ID: {result['details']['columns']['id_column']}")
            print(f"      - Target: {result['details']['columns']['target_column']}")
            print(f"      - Features: {len(result['details']['columns']['feature_columns'])}")
            print(f"      - Topics: {len(result['details']['columns']['topic_columns'])}")
        else:
            print(f"❌ Upload failed: {response.text}")
            sys.exit(1)
except FileNotFoundError:
    print("❌ students.csv not found in current directory")
    print("   Please make sure students.csv exists or use a different CSV file")
    sys.exit(1)

# Test the advisor
print("\n💬 Testing AI Advisor...")

query_data = {
    "query": "Which students need intervention?",
    "dataset_id": "default"
}

response = requests.post(
    f"{BASE_URL}/ask_advisor",
    json=query_data
)

if response.status_code == 200:
    result = response.json()
    print("✅ AI Advisor is working!")
    print(f"   Response Type: {result['response_type']}")
    print(f"   Message preview: {result['message'][:100]}...")
else:
    print(f"❌ AI Advisor test failed: {response.text}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ SETUP COMPLETE!")
print("=" * 70)
print("\nYour frontend should now work with the 'default' dataset.")
print("\nYou can now:")
print("1. Use the frontend at http://localhost:5173/advisor")
print("2. Ask questions like:")
print("   - 'Which students need intervention?'")
print("   - 'Why is student 29 at risk?'")
print("   - 'Generate quiz for student 5'")
print("\nTo upload additional datasets:")
print("   curl -X POST 'http://localhost:8000/upload_csv' \\")
print("     -F 'file=@your_file.csv' \\")
print("     -F 'dataset_id=your_dataset_id'")
