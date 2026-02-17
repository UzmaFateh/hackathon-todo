import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

# Note: This script requires a valid JWT token. 
# In a real scenario, we'd sign in first/again.
# For simplicity, we'll try to sign in as the user we created earlier.

def test_analytics():
    print("Testing Analytics API...")
    
    # 1. Sign In
    email = "uzma...9@gmail.com" # Using the user we saw in DB earlier, assuming password is known or we'll create a new one
    # Actually, better to create a new user to be sure
    import uuid
    email = f"analytics_test_{uuid.uuid4()}@example.com"
    password = "password123"
    
    print(f"Signing up new user {email}...")
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/sign-up", json={
            "email": email,
            "password": password,
            "name": "Analytics Tester"
        })
        if resp.status_code == 201:
            token = resp.json().get("token")
        else:
            print(f"❌ Sign Up Failed: {resp.status_code} {resp.text}")
            return
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create some tasks
    tasks = [
        {"title": "Finish the report", "priority": "high", "is_completed": False},
        {"title": "Email the team", "priority": "medium", "is_completed": True},
        {"title": "Buy groceries", "priority": "low", "is_completed": False}
    ]
    
    print("Creating sample tasks...")
    for t in tasks:
        requests.post(f"{BASE_URL}/api/tasks", json=t, headers=headers)

    # 3. Call Analytics
    print("Calling Analytics Endpoint...")
    try:
        resp = requests.post(f"{BASE_URL}/api/analytics/", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            print("✅ Analytics Response Received:")
            print(data.get("insight"))
        elif resp.status_code == 500 and "Gemini API Key" in resp.text:
             print("⚠️ Analytics Failed (Expected if key is placeholder):")
             print(resp.text)
        else:
            print(f"❌ Analytics Failed: {resp.status_code} {resp.text}")

    except Exception as e:
        print(f"❌ Analytics Error: {e}")

if __name__ == "__main__":
    test_analytics()
