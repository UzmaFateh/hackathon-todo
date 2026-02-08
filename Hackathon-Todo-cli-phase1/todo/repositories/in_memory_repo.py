from typing import List, Optional, Dict
from todo.models.task import Task, TaskFilter, Priority
import uuid


class InMemoryTaskRepository:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def create(self, task: Task) -> Task:
        """Create a new task and store it."""
        self._tasks[task.id] = task
        return task

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)

    def update(self, task_id: str, updated_task: Task) -> Optional[Task]:
        """Update an existing task."""
        if task_id in self._tasks:
            self._tasks[task_id] = updated_task
            return updated_task
        return None

    def delete(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def list_all(self) -> List[Task]:
        """Retrieve all tasks."""
        return list(self._tasks.values())

    def search(self, filter_obj: TaskFilter) -> List[Task]:
        """Search and filter tasks based on the provided filter."""
        tasks = list(self._tasks.values())

        # Filter by status
        if filter_obj.status:
            if filter_obj.status.lower() == "completed":
                tasks = [task for task in tasks if task.completed]
            elif filter_obj.status.lower() == "incomplete":
                tasks = [task for task in tasks if not task.completed]
            # If status is "all" or any other value, don't filter by status

        # Filter by priority
        if filter_obj.priority:
            tasks = [task for task in tasks if task.priority == filter_obj.priority]

        # Filter by tags
        if filter_obj.tags:
            for tag in filter_obj.tags:
                tasks = [task for task in tasks if tag in task.tags]

        # Search by keyword in title or description
        if filter_obj.search_term:
            search_term = filter_obj.search_term.lower()
            tasks = [
                task for task in tasks
                if search_term in task.title.lower() or
                (task.description and search_term in task.description.lower())
            ]

        return tasks