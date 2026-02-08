"""
MCP (Model Context Protocol) tools for todo operations using mcp-todo-skill.

This module implements the MCP tools for managing todos using the
mcp-todo-skill patterns as required by the specification.
"""
import asyncio
from typing import Dict, Any, List, Optional
import uuid
from sqlmodel import Session, select
from db import engine
from models import User, Task


def add_todo(title: str, user_id: str, description: str = None, priority: str = "medium") -> Dict[str, Any]:
    """
    Add a new todo using mcp-todo-skill patterns.

    Args:
        title: Title of the task
        user_id: ID of the user (for validation)
        description: Optional description
        priority: Task priority (high, medium, low)

    Returns:
        Dict with success status and task information
    """
    try:
        # Validate inputs
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "error_code": "MISSING_USER_ID"
            }

        if not title or not title.strip():
            return {
                "success": False,
                "error": "Task title is required",
                "error_code": "MISSING_TITLE"
            }

        try:
            uuid.UUID(user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "error_code": "INVALID_USER_ID"
            }

        with Session(engine) as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return {
                    "success": False,
                    "error": "User not found",
                    "error_code": "USER_NOT_FOUND"
                }

            # Create new task
            task = Task(
                user_id=user_id,
                title=title.strip(),
                priority=priority if priority in ["high", "medium", "low"] else "medium",
                is_completed=False

            )
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": "Task added successfully",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.is_completed,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "DATABASE_ERROR"
        }


def list_todos(user_id: str, status: str = "all") -> Dict[str, Any]:
    """
    List todos for a user using mcp-todo-skill patterns.

    Args:
        user_id: ID of the user
        status: Filter status ("all", "pending", "completed")

    Returns:
        Dict with list of tasks
    """
    try:
        # Validate inputs
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "error_code": "MISSING_USER_ID"
            }

        try:
            uuid.UUID(user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "error_code": "INVALID_USER_ID"
            }

        with Session(engine) as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return {
                    "success": False,
                    "error": "User not found",
                    "error_code": "USER_NOT_FOUND"
                }

            # Query tasks based on status filter
            query = select(Task).where(Task.user_id == user_id)
            
            if status == "pending":
                query = query.where(Task.is_completed == False)
            elif status == "completed":
                query = query.where(Task.is_completed == True)
            
            tasks = session.exec(query).all()

            return {
                "success": True,
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "completed": task.is_completed,
                        "priority": task.priority,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    }
                    for task in tasks
                ],
                "total": len(tasks)
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "DATABASE_ERROR"
        }


def update_todo(task_id: int, user_id: str, title: str = None, priority: str = None, completed: bool = None) -> Dict[str, Any]:
    """
    Update a todo using mcp-todo-skill patterns.

    Args:
        task_id: ID of the task to update
        user_id: ID of the user (for validation)
        title: New title (optional)
        priority: New priority (optional)
        completed: New completed status (optional)

    Returns:
        Dict with success status and updated task information
    """
    try:
        # Validate inputs
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "error_code": "MISSING_USER_ID"
            }

        if task_id is None:
            return {
                "success": False,
                "error": "Task ID is required",
                "error_code": "MISSING_TASK_ID"
            }

        try:
            uuid.UUID(user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "error_code": "INVALID_USER_ID"
            }

        with Session(engine) as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return {
                    "success": False,
                    "error": "User not found",
                    "error_code": "USER_NOT_FOUND"
                }

            # Get the task and verify it belongs to the user
            task = session.get(Task, task_id)
            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "error_code": "TASK_NOT_FOUND"
                }

            if task.user_id != user_id:
                return {
                    "success": False,
                    "error": "Access denied: Task does not belong to user",
                    "error_code": "ACCESS_DENIED"
                }

            # Update fields
            if title is not None and title.strip():
                task.title = title.strip()
            if priority is not None and priority in ["high", "medium", "low"]:
                task.priority = priority
            if completed is not None:
                task.is_completed = completed

            task.update_timestamp()
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": "Task updated successfully",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.is_completed,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "DATABASE_ERROR"
        }


def complete_todo(task_id: int, user_id: str) -> Dict[str, Any]:
    """
    Mark a todo as completed using mcp-todo-skill patterns.

    Args:
        task_id: ID of the task to mark as completed
        user_id: ID of the user (for validation)

    Returns:
        Dict with success status and task information
    """
    try:
        # Validate inputs
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "error_code": "MISSING_USER_ID"
            }

        if task_id is None:
            return {
                "success": False,
                "error": "Task ID is required",
                "error_code": "MISSING_TASK_ID"
            }

        try:
            uuid.UUID(user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "error_code": "INVALID_USER_ID"
            }

        return update_todo(task_id, user_id, completed=True)

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "DATABASE_ERROR"
        }


def delete_todo(task_id: int, user_id: str) -> Dict[str, Any]:
    """
    Delete a todo using mcp-todo-skill patterns.

    Args:
        task_id: ID of the task to delete
        user_id: ID of the user (for validation)

    Returns:
        Dict with success status
    """
    try:
        # Validate inputs
        if not user_id:
            return {
                "success": False,
                "error": "User ID is required",
                "error_code": "MISSING_USER_ID"
            }

        if task_id is None:
            return {
                "success": False,
                "error": "Task ID is required",
                "error_code": "MISSING_TASK_ID"
            }

        try:
            uuid.UUID(user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "error_code": "INVALID_USER_ID"
            }

        with Session(engine) as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return {
                    "success": False,
                    "error": "User not found",
                    "error_code": "USER_NOT_FOUND"
                }

            # Get the task and verify it belongs to the user
            task = session.get(Task, task_id)
            if not task:
                return {
                    "success": False,
                    "error": "Task not found",
                    "error_code": "TASK_NOT_FOUND"
                }

            if task.user_id != user_id:
                return {
                    "success": False,
                    "error": "Access denied: Task does not belong to user",
                    "error_code": "ACCESS_DENIED"
                }

            # Delete the task
            session.delete(task)
            session.commit()

            return {
                "success": True,
                "message": "Task deleted successfully"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "DATABASE_ERROR"
        }


# Export functions that will be registered with the MCP server
__all__ = ["add_todo", "list_todos", "update_todo", "complete_todo", "delete_todo"]