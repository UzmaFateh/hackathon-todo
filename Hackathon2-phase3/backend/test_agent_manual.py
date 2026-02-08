import asyncio
import os
import uuid
from dotenv import load_dotenv, find_dotenv
from sqlmodel import Session, select
from db import engine, init_db
from models import User, Task
from ai_agents.chat_agent import create_agent, ChatAgentRunner

# Load environment variables
load_dotenv(find_dotenv())

async def test_agent():
    print("--- Initializing DB ---")
    init_db()
    
    # Create a test user
    user_id = str(uuid.uuid4())
    print(f"--- Creating Test User: {user_id} ---")
    
    with Session(engine) as session:
        user = User(id=user_id, email=f"test_{user_id[:8]}@example.com", password_hash="hash")
        session.add(user)
        session.commit()
        
    # Create agent
    print("--- Creating Agent ---")
    try:
        agent = create_agent(user_id)
    except Exception as e:
        print(f"Failed to create agent: {e}")
        return

    # Test 1: Add a task
    print("\n--- Test 1: Add Task ---")
    message = "Add a task to buy milk"
    print(f"User: {message}")
    
    response = await ChatAgentRunner.process_message(agent, message)
    print(f"Agent: {response['response']}")
    
    # Verify in DB
    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        print(f"DB Tasks: {[t.title for t in tasks]}")
        assert len(tasks) == 1
        assert tasks[0].title == "buy milk" or "buy milk" in tasks[0].title.lower()

    # Test 2: List tasks
    print("\n--- Test 2: List Tasks ---")
    message = "List my tasks"
    print(f"User: {message}")
    
    response = await ChatAgentRunner.process_message(agent, message)
    print(f"Agent: {response['response']}")
    assert "buy milk" in response['response'].lower()

    # Test 3: Complete task
    print("\n--- Test 3: Complete Task ---")
    # We need the ID, but the agent should handle it if we say "complete task 1" assuming it listed it as 1.
    # Let's assume the list output format is "ID. [ ] Title"
    message = f"Complete task {tasks[0].id}"
    print(f"User: {message}")
    
    response = await ChatAgentRunner.process_message(agent, message)
    print(f"Agent: {response['response']}")
    
    # Verify in DB
    with Session(engine) as session:
        task = session.get(Task, tasks[0].id)
        print(f"Task Completed: {task.is_completed}")
        assert task.is_completed == True

    print("\n--- All Tests Passed! ---")

if __name__ == "__main__":
    print("Script started...")
    asyncio.run(test_agent())
