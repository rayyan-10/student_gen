"""
Test script to demonstrate the flexible CSV upload functionality.
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_upload_csv():
    """Test uploading the existing students.csv file."""
    print("=" * 60)
    print("Testing CSV Upload")
    print("=" * 60)
    
    with open("students.csv", "rb") as f:
        files = {"file": ("students.csv", f, "text/csv")}
        data = {"dataset_id": "students_2024"}
        
        response = requests.post(f"{BASE_URL}/upload_csv", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Upload successful!")
            print(f"  Dataset ID: {result['details']['dataset_id']}")
            print(f"  Rows: {result['details']['rows']}")
            print(f"  Model Accuracy: {result['details']['model_accuracy']}")
            print(f"  Detected Columns:")
            print(f"    - ID Column: {result['details']['columns']['id_column']}")
            print(f"    - Target Column: {result['details']['columns']['target_column']}")
            print(f"    - Feature Columns: {len(result['details']['columns']['feature_columns'])}")
            print(f"    - Topic Columns: {len(result['details']['columns']['topic_columns'])}")
        else:
            print(f"✗ Upload failed: {response.text}")
    
    print()


def test_list_datasets():
    """Test listing all datasets."""
    print("=" * 60)
    print("Listing All Datasets")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/datasets")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Total datasets: {result['total']}")
        for ds in result['datasets']:
            print(f"\n  Dataset: {ds['dataset_id']}")
            print(f"    Rows: {ds['rows']}")
            print(f"    Columns: {ds['columns']}")
            print(f"    Accuracy: {ds['accuracy']}")
    else:
        print(f"✗ Failed: {response.text}")
    
    print()


def test_ask_advisor():
    """Test asking the advisor questions."""
    print("=" * 60)
    print("Testing AI Advisor")
    print("=" * 60)
    
    queries = [
        "Which records need intervention?",
        "Why is student 5 at risk?",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        
        response = requests.post(
            f"{BASE_URL}/ask_advisor",
            json={"query": query, "dataset_id": "students_2024"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response Type: {result['response_type']}")
            print(f"Message: {result['message'][:200]}...")
        else:
            print(f"✗ Failed: {response.text}")
    
    print()


def test_get_records():
    """Test getting all records with predictions."""
    print("=" * 60)
    print("Getting All Records")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/records/students_2024")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Total records: {result['total']}")
        
        # Show first 3 records
        print("\nFirst 3 records:")
        for record in result['records'][:3]:
            print(f"\n  ID: {record['id']}")
            print(f"    Pass Probability: {record['pass_probability']:.2%}")
            print(f"    Risk Level: {record['risk_level']}")
            print(f"    Weak Areas: {', '.join(record['weak_areas']) if record['weak_areas'] else 'None'}")
    else:
        print(f"✗ Failed: {response.text}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DYNAMIC CSV UPLOAD TEST SUITE")
    print("=" * 60)
    print("\nMake sure the server is running:")
    print("  uvicorn app.main:app --reload")
    print()
    
    try:
        # Test if server is running
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("✗ Server is not responding. Please start it first.")
            exit(1)
        
        # Run tests
        test_upload_csv()
        test_list_datasets()
        test_ask_advisor()
        test_get_records()
        
        print("=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Please start it with:")
        print("  uvicorn app.main:app --reload")
