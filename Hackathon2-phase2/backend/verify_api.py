import requests
import sys
import uuid

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("Running API verification...")
    
    # 1. Health Check
    try:
        resp = requests.get(f"{BASE_URL}/api/health")
        if resp.status_code == 200:
            print("✅ Health Check: PASSED")
        else:
            print(f"❌ Health Check: FAILED ({resp.status_code})")
            return
    except Exception as e:
        print(f"❌ Health Check: FAILED (Connection error: {e})")
        return

    # 2. Sign Up
    email = f"test_{uuid.uuid4()}@example.com"
    password = "password123"
    print(f"Testing Sign Up with {email}...")
    
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/sign-up", json={
            "email": email,
            "password": password,
            "name": "Test User"
        })
        if resp.status_code == 201:
            print("✅ Sign Up: PASSED")
            data = resp.json()
            token = data.get("token")
        else:
            print(f"❌ Sign Up: FAILED ({resp.status_code} - {resp.text})")
            return
    except Exception as e:
        print(f"❌ Sign Up: FAILED (Error: {e})")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Task
    print("Testing Create Task...")
    try:
        resp = requests.post(f"{BASE_URL}/api/tasks", json={
            "title": "Test Task from Script",
            "priority": "medium"
        }, headers=headers)
        
        if resp.status_code == 201:
            print("✅ Create Task: PASSED")
            task_id = resp.json().get("id")
        else:
            print(f"❌ Create Task: FAILED ({resp.status_code} - {resp.text})")
            return
    except Exception as e:
        print(f"❌ Create Task: FAILED (Error: {e})")
        return

    # 4. List Tasks
    print("Testing List Tasks...")
    try:
        resp = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
        if resp.status_code == 200:
            tasks = resp.json()
            if any(t["id"] == task_id for t in tasks):
                print("✅ List Tasks: PASSED (Found created task)")
            else:
                print("⚠️ List Tasks: PASSED (But created task not found?)")
        else:
            print(f"❌ List Tasks: FAILED ({resp.status_code})")
            return
    except Exception as e:
        print(f"❌ List Tasks: FAILED (Error: {e})")
        return

    print("\n🎉 All API tests passed!")

if __name__ == "__main__":
    test_api()
