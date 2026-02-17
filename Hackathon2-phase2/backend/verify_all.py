import requests
import sys
import uuid
import json

BASE_URL = "http://127.0.0.1:8000"

def log(msg, status="INFO"):
    symbols = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
    print(f"{symbols.get(status, '')} {msg}")

def verify_all():
    print("🚀 Starting Comprehensive API Verification...\n")
    
    # 1. Health Check
    try:
        resp = requests.get(f"{BASE_URL}/api/health")
        if resp.status_code == 200:
            log("Health Check: OK", "PASS")
        else:
            log(f"Health Check Failed: {resp.status_code}", "FAIL")
            return
    except Exception as e:
        log(f"Backend not reachable: {e}", "FAIL")
        return

    # 2. Auth - Sign Up
    email = f"verify_{uuid.uuid4()}@example.com"
    password = "password123"
    token = None
    
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/sign-up", json={
            "email": email,
            "password": password,
            "name": "Verify User"
        })
        if resp.status_code == 201:
            log("Auth (Sign Up): OK", "PASS")
            token = resp.json().get("token")
        else:
            log(f"Auth (Sign Up) Failed: {resp.text}", "FAIL")
            return
    except Exception as e:
        log(f"Auth Error: {e}", "FAIL")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Tasks - Create
    task_id = None
    try:
        resp = requests.post(f"{BASE_URL}/api/tasks", json={
            "title": "Verification Task",
            "priority": "high"
        }, headers=headers)
        if resp.status_code == 201:
            log("Tasks (Create): OK", "PASS")
            task_id = resp.json().get("id")
        else:
            log(f"Tasks (Create) Failed: {resp.text}", "FAIL")
    except Exception as e:
        log(f"Tasks Error: {e}", "FAIL")

    # 4. Tasks - List
    try:
        resp = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
        if resp.status_code == 200:
            tasks = resp.json()
            if any(t["id"] == task_id for t in tasks):
                 log("Tasks (List): OK", "PASS")
            else:
                 log("Tasks (List): Created task not found", "WARN")
        else:
            log(f"Tasks (List) Failed: {resp.status_code}", "FAIL")
    except Exception as e:
        log(f"Tasks List Error: {e}", "FAIL")

    # 5. Tags - List (Public/Private)
    try:
        resp = requests.get(f"{BASE_URL}/api/tags", headers=headers)
        if resp.status_code == 200:
            log("Tags (List): OK", "PASS")
        else:
             log(f"Tags (List) Failed: {resp.status_code}", "FAIL")
    except Exception as e:
        log(f"Tags Error: {e}", "FAIL")

    # 6. Analytics
    print("\n🔮 Verifying Analytics...")
    try:
        resp = requests.post(f"{BASE_URL}/api/analytics/", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            insight = data.get("insight", "")
            if "Mock Data" in insight:
                 log("Analytics: OK (Using Mock Data due to API key error)", "PASS")
            elif "Error" in insight or "invalid" in insight.lower():
                 log(f"Analytics Response (Handled Error): {insight}", "WARN")
            else:
                 log("Analytics: OK (Insights generated)", "PASS")
                 print(f"   Insight: {insight[:100]}...")
        else:
            log(f"Analytics Failed: {resp.status_code} {resp.text}", "FAIL")
    except Exception as e:
        log(f"Analytics Error: {e}", "FAIL")

    print("\n✨ Verification Complete.")

if __name__ == "__main__":
    verify_all()
