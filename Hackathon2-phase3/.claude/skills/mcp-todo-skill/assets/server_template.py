from sqlmodel import Field, SQLModel, Session, create_engine, select
from typing import Optional, List
from mcp.server.fastmcp import FastMCP
import os

# --- Configuration ---
# Use project-standard DATABASE_URL env var
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/todo_db")

# --- Models ---
# Define minimal models needed for the tools.
# In a real project, import these from backend.models to share schema.
class TodoTask(SQLModel, table=True):
    __tablename__ = "todos"  # Adjust table name to match production schema
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    status: str = Field(default="pending")

# --- Database Setup ---
engine = create_engine(DATABASE_URL)

def get_session():
    """Dependency for database session."""
    return Session(engine)

# --- MCP Server ---
mcp = FastMCP("Todo Manager")

# --- Tools ---

@mcp.tool()
def add_task(user_id: str, title: str) -> dict:
    """
    Add a new todo task for a user.

    Args:
        user_id: The ID of the authenticated user.
        title: The description of the task.
    """
    with get_session() as session:
        task = TodoTask(user_id=user_id, title=title)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task.model_dump()

@mcp.tool()
def list_tasks(user_id: str, status: str = None) -> List[dict]:
    """
    List all tasks for a user, optionally filtering by status.

    Args:
        user_id: The ID of the authenticated user.
        status: Optional status to filter by (e.g., 'pending', 'completed').
    """
    with get_session() as session:
        query = select(TodoTask).where(TodoTask.user_id == user_id)
        if status:
            query = query.where(TodoTask.status == status)

        results = session.exec(query).all()
        return [task.model_dump() for task in results]

@mcp.tool()
def complete_task(user_id: str, task_id: int) -> dict:
    """
    Mark a task as completed.

    Args:
        user_id: The ID of the authenticated user.
        task_id: The ID of the task to complete.
    """
    with get_session() as session:
        task = session.exec(
            select(TodoTask).where(TodoTask.id == task_id, TodoTask.user_id == user_id)
        ).first()

        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")

        task.status = "completed"
        session.add(task)
        session.commit()
        session.refresh(task)
        return task.model_dump()

@mcp.tool()
def delete_task(user_id: str, task_id: int) -> dict:
    """
    Delete a task permanently.

    Args:
        user_id: The ID of the authenticated user.
        task_id: The ID of the task to delete.
    """
    with get_session() as session:
        task = session.exec(
            select(TodoTask).where(TodoTask.id == task_id, TodoTask.user_id == user_id)
        ).first()

        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")

        session.delete(task)
        session.commit()
        return {"status": "deleted", "id": task_id}

@mcp.tool()
def update_task(user_id: str, task_id: int, title: str = None) -> dict:
    """
    Update a task's title.

    Args:
        user_id: The ID of the authenticated user.
        task_id: The ID of the task to update.
        title: The new title for the task (optional).
    """
    with get_session() as session:
        task = session.exec(
            select(TodoTask).where(TodoTask.id == task_id, TodoTask.user_id == user_id)
        ).first()

        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")

        if title:
            task.title = title

        session.add(task)
        session.commit()
        session.refresh(task)
        return task.model_dump()

if __name__ == "__main__":
    # Standard MCP entry point
    mcp.run()
