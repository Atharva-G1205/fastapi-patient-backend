"""
Test script for the Combined Patient Management API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_basic_endpoints():
    """Test basic endpoints"""
    print("Testing basic endpoints...")
    
    response = requests.get(f"{BASE_URL}/")
    print(f"GET /: {response.status_code} - {response.json()}")
    
    response = requests.get(f"{BASE_URL}/about")
    print(f"GET /about: {response.status_code} - {response.json()}")
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"GET /health: {response.status_code} - {response.json()}")

def test_patient_endpoints():
    """Test patient management endpoints"""
    print("\nTesting patient endpoints...")

    response = requests.get(f"{BASE_URL}/patients")
    print(f"GET /patients: {response.status_code}")
    
    response = requests.get(f"{BASE_URL}/patients/P001")
    print(f"GET /patients/P001: {response.status_code}")
    
    response = requests.get(f"{BASE_URL}/patients/sort/by?sort_by=bmi&order=desc")
    print(f"GET /patients/sort/by: {response.status_code}")

def test_crud_operations():
    """Test CRUD operations"""
    print("\nTesting CRUD operations...")
    
    new_patient = {
        "id": "P999",
        "name": "Test Patient",
        "city": "Test City",
        "age": 25,
        "gender": "male",
        "height": 1.75,
        "weight": 70
    }
    
    response = requests.post(f"{BASE_URL}/patients", json=new_patient)
    print(f"POST /patients: {response.status_code}")
    
    if response.status_code == 201:

        update_data = {
            "age": 26,
            "weight": 72
        }
        response = requests.put(f"{BASE_URL}/patients/P999", json=update_data)
        print(f"PUT /patients/P999: {response.status_code}")
        

        response = requests.delete(f"{BASE_URL}/patients/P999")
        print(f"DELETE /patients/P999: {response.status_code}")

if __name__ == "__main__":
    try:
        print("Combined Patient Management API Test")
        print("=" * 40)
        
        test_basic_endpoints()
        test_patient_endpoints()
        test_crud_operations()
        
        print("\nTest completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")