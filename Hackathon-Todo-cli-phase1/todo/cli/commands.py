import typer
from typing import List, Optional
from todo.models.task import Task, Priority, TaskFilter
from todo.services.task_service import TaskService
from todo.repositories.in_memory_repo import InMemoryTaskRepository
from rich.table import Table
from rich.console import Console


def create_add_command(task_service: TaskService):
    def add_task(
        title: str = typer.Option(..., help="Task title (required, min 1 char, max 255 chars)"),
        description: Optional[str] = typer.Option(None, help="Task description (max 1000 chars)"),
        priority: Priority = typer.Option(Priority.MEDIUM, help="Task priority (high/medium/low)"),
        tags: List[str] = typer.Option([], help="Task tags (max 10 per task, max 50 chars each)")
    ):
        """
        Add a new task with title, description, priority, and tags.
        """
        try:
            task = task_service.create_task(
                title=title,
                description=description,
                priority=priority,
                tags=tags
            )
            typer.echo(f"Task created successfully with ID: {task.id}")
        except ValueError as e:
            typer.echo(f"Error: Invalid input - {str(e)}", err=True)
            raise typer.Exit(code=1)

    return add_task


def create_list_command(task_service: TaskService):
    def list_tasks(
        status: Optional[str] = typer.Option(None, help="Filter by completion status (completed, incomplete, all)"),
        priority: Optional[Priority] = typer.Option(None, help="Filter by priority (high, medium, low)"),
        search: Optional[str] = typer.Option(None, help="Search keyword to match in title/description"),
        tags: List[str] = typer.Option([], help="Filter by specific tags")
    ):
        """
        List all tasks with optional filtering.
        """
        # Create filter object based on provided parameters
        filter_obj = TaskFilter(
            status=status,
            priority=priority,
            search_term=search,
            tags=tags if tags else None
        )

        tasks = task_service.list_tasks(filter_obj)

        if not tasks:
            typer.echo("No tasks found.")
            return

        # Create a rich table to display tasks
        console = Console()
        table = Table(title="Tasks")
        table.add_column("ID", style="dim", width=36)  # UUID length
        table.add_column("Title")
        table.add_column("Status")
        table.add_column("Priority")
        table.add_column("Tags")
        table.add_column("Created")

        for task in tasks:
            status = "✓ Completed" if task.completed else "○ Incomplete"
            priority_str = task.priority.value
            tags_str = ", ".join(task.tags) if task.tags else "None"
            created_str = task.created_at.strftime("%Y-%m-%d %H:%M")

            table.add_row(
                task.id,
                task.title,
                status,
                priority_str,
                tags_str,
                created_str
            )

        console.print(table)

    return list_tasks


def create_update_command(task_service: TaskService):
    def update_task(
        task_id: str = typer.Argument(..., help="Task ID to update"),
        title: Optional[str] = typer.Option(None, help="New title"),
        description: Optional[str] = typer.Option(None, help="New description"),
        priority: Optional[Priority] = typer.Option(None, help="New priority (high/medium/low)"),
        tags: List[str] = typer.Option(None, help="New list of tags")
    ):
        """
        Update an existing task.
        """
        try:
            updated_task = task_service.update_task(
                task_id=task_id,
                title=title,
                description=description,
                priority=priority,
                tags=tags
            )

            if updated_task:
                typer.echo("Task updated successfully")
            else:
                typer.echo(f"Error: Task with ID {task_id} not found", err=True)
                raise typer.Exit(code=3)
        except ValueError as e:
            typer.echo(f"Error: Invalid input - {str(e)}", err=True)
            raise typer.Exit(code=1)

    return update_task


def create_complete_command(task_service: TaskService):
    def complete_task(
        task_id: str = typer.Argument(..., help="Task ID to update"),
        status: bool = typer.Option(True, help="Completion status (default: true)")
    ):
        """
        Mark task as complete or incomplete.
        """
        task = task_service.get_task(task_id)
        if not task:
            typer.echo(f"Error: Task with ID {task_id} not found", err=True)
            raise typer.Exit(code=3)

        updated_task = task_service.complete_task(task_id, status)
        if updated_task:
            status_text = "completed" if status else "incomplete"
            typer.echo(f"Task marked as {status_text}")
        else:
            typer.echo(f"Error: Task with ID {task_id} not found", err=True)
            raise typer.Exit(code=3)

    return complete_task


def create_delete_command(task_service: TaskService):
    def delete_task(
        task_id: str = typer.Argument(..., help="Task ID to delete")
    ):
        """
        Delete a task by its ID.
        """
        success = task_service.delete_task(task_id)
        if success:
            typer.echo("Task deleted successfully")
        else:
            typer.echo(f"Error: Task with ID {task_id} not found", err=True)
            raise typer.Exit(code=3)

    return delete_task