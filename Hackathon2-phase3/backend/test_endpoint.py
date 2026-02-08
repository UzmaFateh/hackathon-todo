import asyncio
import os
import uuid
import httpx
from dotenv import load_dotenv, find_dotenv
from sqlmodel import Session
from db import engine, init_db
from models import User

# Load environment variables
load_dotenv(find_dotenv())

BASE_URL = "http://127.0.0.1:8000"

async def test_endpoint():
    print("--- Testing API ---")
    
    # Check health
    health_url = f"{BASE_URL}/api/health"
    print(f"Checking health at {health_url}...")
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(health_url)
            print(f"Health Status: {resp.status_code}")
            if resp.status_code != 200:
                print("Server is not healthy or not running.")
                return
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return

    # 1. Create a test user directly in DB to ensure valid ID
    user_id = str(uuid.uuid4())
    print(f"Creating test user: {user_id}")
    
    # Ensure DB is initialized (safe to run multiple times)
    try:
        init_db()
        with Session(engine) as session:
            user = User(id=user_id, email=f"test_api_{user_id[:8]}@example.com", password_hash="hash")
            session.add(user)
            session.commit()
    except Exception as e:
        print(f"DB Error: {e}")
        return
        
    # 2. Send request to chat endpoint
    url = f"{BASE_URL}/api/{user_id}/chat"
    payload = {
        "message": "Add a task to call mom"
    }
    
    print(f"Sending POST to {url} with payload: {payload}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, json=payload)
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Success! Agent response: {data.get('response')}")
                assert data.get('success') == True
            else:
                print("Request failed.")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting test script...")
    asyncio.run(test_endpoint())
