import httpx
import asyncio
import sys

async def main():
    with open("e:/CODING/Hackathon2-Phase3/test_result.txt", "w") as f:
        f.write("Starting test...\n")
        try:
            async with httpx.AsyncClient() as client:
                f.write("Checking health...\n")
                resp = await client.get("http://127.0.0.1:8000/api/health")
                f.write(f"Health: {resp.status_code}\n")
                
                # If health is good, try chat
                if resp.status_code == 200:
                    # We need a user_id. Let's just use a dummy one and expect 404 or 500 if user not found, 
                    # but at least we hit the endpoint.
                    # Or we can try to create a user if we import the models.
                    # But let's keep it simple.
                    f.write("Checking chat endpoint...\n")
                    # We expect 404 for user not found, which confirms endpoint is reachable
                    resp = await client.post("http://127.0.0.1:8000/api/dummy-user/chat", json={"message": "hi"})
                    f.write(f"Chat Response: {resp.status_code}\n")
                    f.write(f"Chat Body: {resp.text}\n")
                
        except Exception as e:
            f.write(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
