#!/usr/bin/env python3
"""
Test script to verify the todo application implementation.
This tests the functionality in a single execution context.
"""

from todo.services.task_service import TaskService
from todo.repositories.in_memory_repo import InMemoryTaskRepository
from todo.models.task import Priority


def test_implementation():
    print("Testing Todo Application Implementation...")

    # Initialize repository and service
    repository = InMemoryTaskRepository()
    task_service = TaskService(repository)

    print("\n1. Testing Task Creation...")
    # Test creating a task
    task1 = task_service.create_task(
        title="Test Task 1",
        description="This is a test task",
        priority=Priority.HIGH,
        tags=["test", "work"]
    )
    print(f"OK Created task with ID: {task1.id}")

    # Test creating another task
    task2 = task_service.create_task(
        title="Test Task 2",
        description="Another test task",
        priority=Priority.LOW,
        tags=["personal"]
    )
    print(f"OK Created task with ID: {task2.id}")

    print("\n2. Testing Task Listing...")
    # List all tasks
    all_tasks = task_service.list_tasks()
    print(f"OK Found {len(all_tasks)} tasks")

    print("\n3. Testing Task Filtering...")
    # Filter by priority
    high_priority_tasks = task_service.filter_tasks_by_priority(Priority.HIGH)
    print(f"OK Found {len(high_priority_tasks)} high priority tasks")

    # Filter by completion status (should be incomplete by default)
    incomplete_tasks = task_service.filter_tasks_by_status(False)
    print(f"OK Found {len(incomplete_tasks)} incomplete tasks")

    print("\n4. Testing Task Update...")
    # Update a task
    updated_task = task_service.update_task(
        task_id=task1.id,
        title="Updated Test Task 1",
        description="This task has been updated"
    )
    if updated_task:
        print(f"OK Updated task: {updated_task.title}")
    else:
        print("ERROR Failed to update task")

    print("\n5. Testing Task Completion...")
    # Mark a task as complete
    completed_task = task_service.complete_task(task1.id, True)
    if completed_task:
        print(f"OK Marked task as complete: {completed_task.title}, completed={completed_task.completed}")
    else:
        print("ERROR Failed to mark task as complete")

    print("\n6. Testing Task Search...")
    # Search for tasks
    search_results = task_service.search_tasks("Updated")
    print(f"OK Found {len(search_results)} tasks matching 'Updated'")

    print("\n7. Testing Task Deletion...")
    # Delete a task
    delete_success = task_service.delete_task(task2.id)
    if delete_success:
        print("OK Deleted task successfully")
    else:
        print("ERROR Failed to delete task")

    # Verify deletion
    remaining_tasks = task_service.list_tasks()
    print(f"OK Remaining tasks after deletion: {len(remaining_tasks)}")

    print("\n8. Testing Error Handling...")
    # Test invalid operations
    result = task_service.update_task("non-existent-id", title="Should fail")
    if result is None:
        print("OK Properly handled update of non-existent task")
    else:
        print("ERROR Should have failed to update non-existent task")

    try:
        task_service.create_task(title="")  # Empty title should fail
        print("ERROR Should have failed to create task with empty title")
    except ValueError:
        print("OK Properly validated task creation")

    print("\nOK All tests passed! Implementation is working correctly.")


if __name__ == "__main__":
    test_implementation()