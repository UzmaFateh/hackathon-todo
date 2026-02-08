from typing import List, Optional
from todo.models.task import Task, TaskFilter, Priority
from todo.repositories.in_memory_repo import InMemoryTaskRepository
import uuid


class TaskService:
    def __init__(self, repository: InMemoryTaskRepository):
        self.repository = repository

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None
    ) -> Task:
        """Create a new task with validation."""
        # Validate title
        if not title or len(title) < 1 or len(title) > 255:
            raise ValueError("Title must be between 1 and 255 characters")

        # Validate description if provided
        if description and len(description) > 1000:
            raise ValueError("Description must not exceed 1000 characters")

        # Validate tags if provided
        if tags:
            if len(tags) > 10:
                raise ValueError("A task cannot have more than 10 tags")
            for tag in tags:
                if len(tag) > 50:
                    raise ValueError("Each tag must not exceed 50 characters")
            # Check for duplicate tags
            if len(tags) != len(set(tags)):
                raise ValueError("Duplicate tags detected")

        # Generate unique ID
        task_id = str(uuid.uuid4())

        # Create and save the task
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or []
        )
        return self.repository.create(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        return self.repository.get_by_id(task_id)

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Task]:
        """Update an existing task."""
        existing_task = self.repository.get_by_id(task_id)
        if not existing_task:
            return None

        # Validate fields if provided
        if title is not None:
            if not title or len(title) < 1 or len(title) > 255:
                raise ValueError("Title must be between 1 and 255 characters")

        if description is not None and len(description) > 1000:
            raise ValueError("Description must not exceed 1000 characters")

        if tags is not None:
            if len(tags) > 10:
                raise ValueError("A task cannot have more than 10 tags")
            for tag in tags:
                if len(tag) > 50:
                    raise ValueError("Each tag must not exceed 50 characters")
            # Check for duplicate tags
            if len(tags) != len(set(tags)):
                raise ValueError("Duplicate tags detected")

        # Update fields that were provided
        if title is not None:
            existing_task.title = title
        if description is not None:
            existing_task.description = description
        if priority is not None:
            existing_task.priority = priority
        if tags is not None:
            existing_task.tags = tags

        return self.repository.update(task_id, existing_task)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID."""
        return self.repository.delete(task_id)

    def list_tasks(self, filter_obj: Optional[TaskFilter] = None) -> List[Task]:
        """List all tasks, optionally filtered."""
        if filter_obj:
            return self.repository.search(filter_obj)
        return self.repository.list_all()

    def complete_task(self, task_id: str, completed: bool = True) -> Optional[Task]:
        """Mark a task as complete or incomplete."""
        task = self.repository.get_by_id(task_id)
        if task:
            task.completed = completed
            return self.repository.update(task_id, task)
        return None

    def search_tasks(self, search_term: str) -> List[Task]:
        """Search tasks by keyword."""
        filter_obj = TaskFilter(search_term=search_term)
        return self.repository.search(filter_obj)

    def filter_tasks_by_status(self, completed: bool) -> List[Task]:
        """Filter tasks by completion status."""
        status = "completed" if completed else "incomplete"
        filter_obj = TaskFilter(status=status)
        return self.repository.search(filter_obj)

    def filter_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Filter tasks by priority."""
        filter_obj = TaskFilter(priority=priority)
        return self.repository.search(filter_obj)