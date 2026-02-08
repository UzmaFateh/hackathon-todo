from typing import List
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from todo.interactive.menu import MenuItem, MenuState
from todo.interactive.session import SessionState
from todo.services.task_service import TaskService
from todo.models.task import Priority


class MenuController:
    def __init__(self, session_state: SessionState):
        self.session_state = session_state
        self.console = Console()
        self.task_service = session_state.task_service  # type: TaskService

    def display_main_menu(self):
        """Display the main menu with all available operations"""
        self.console.clear()
        self.console.rule("[bold blue]Todo App - Interactive Mode[/bold blue]")

        table = Table(show_header=False, box=None)
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Action", style="white")
        table.add_column("Description", style="dim")

        # Add menu items with numbering
        menu_items = self.get_main_menu_items()
        for idx, item in enumerate(menu_items, 1):
            table.add_row(f"{idx}.", item.title, item.description)

        self.console.print(table)
        self.console.print("\n[navigation]Use number keys to select, 'q' to quit[/navigation]")

    def get_main_menu_items(self) -> List[MenuItem]:
        """Get the main menu items with their actions"""
        return [
            MenuItem(
                id="add",
                title="Add Task",
                description="Create a new task with title, description, priority, and tags",
                action=lambda: self.add_task_action()
            ),
            MenuItem(
                id="list",
                title="List Tasks",
                description="View all tasks with filtering and search options",
                action=lambda: self.list_tasks_action()
            ),
            MenuItem(
                id="update",
                title="Update Task",
                description="Modify an existing task's fields",
                action=lambda: self.update_task_action()
            ),
            MenuItem(
                id="complete",
                title="Complete Task",
                description="Mark a task as complete or incomplete",
                action=lambda: self.complete_task_action()
            ),
            MenuItem(
                id="delete",
                title="Delete Task",
                description="Remove a task permanently",
                action=lambda: self.delete_task_action()
            ),
            MenuItem(
                id="exit",
                title="Exit",
                description="Leave the interactive mode",
                action=lambda: self.exit_action()
            )
        ]

    def add_task_action(self):
        """Action for adding a new task"""
        self.console.clear()
        self.console.rule("[bold]Add New Task[/bold]")

        try:
            title = Prompt.ask("[bold cyan]Title (required)[/bold cyan]")

            description = Prompt.ask("[bold cyan]Description (optional)[/bold cyan]", default="")
            if description == "":
                description = None

            priority_str = Prompt.ask("[bold cyan]Priority ([blue]high[/blue]/[yellow]medium[/yellow]/[red]low[/red])[/bold cyan]",
                                    choices=["high", "medium", "low"], default="medium")
            priority = Priority[priority_str.upper()]

            tags_input = Prompt.ask("[bold cyan]Tags (comma-separated, optional)[/bold cyan]", default="")
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []

            task = self.task_service.create_task(
                title=title,
                description=description,
                priority=priority,
                tags=tags
            )

            self.console.print(f"[green]✓ Task created successfully with ID: {task.id}[/green]")
            self.console.input("\nPress Enter to return to main menu...")

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error creating task: {str(e)}[/red]")
            self.console.input("\nPress Enter to return to main menu...")

    def list_tasks_action(self):
        """Action for listing tasks"""
        self.console.clear()
        self.console.rule("[bold]List Tasks[/bold]")

        try:
            tasks = self.task_service.list_tasks()

            if not tasks:
                self.console.print("[yellow]No tasks found.[/yellow]")
            else:
                table = Table(title="Tasks")
                table.add_column("ID", style="dim", width=36)
                table.add_column("Title")
                table.add_column("Status")
                table.add_column("Priority")
                table.add_column("Tags")
                table.add_column("Created")

                for task in tasks:
                    status = "[green]✓ Completed[/green]" if task.completed else "[red]○ Incomplete[/red]"
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

                self.console.print(table)

            self.console.input("\nPress Enter to return to main menu...")

        except Exception as e:
            self.console.print(f"[red]Error listing tasks: {str(e)}[/red]")
            self.console.input("\nPress Enter to return to main menu...")

    def update_task_action(self):
        """Action for updating a task"""
        self.console.clear()
        self.console.rule("[bold]Update Task[/bold]")

        try:
            task_id = Prompt.ask("[bold cyan]Task ID to update[/bold cyan]")

            # First get the current task to show current values
            current_task = self.task_service.get_task(task_id)
            if not current_task:
                self.console.print(f"[red]Task with ID {task_id} not found.[/red]")
                self.console.input("\nPress Enter to return to main menu...")
                return

            self.console.print(f"[dim]Current values:[/dim]")
            self.console.print(f"  Title: {current_task.title}")
            self.console.print(f"  Description: {current_task.description or 'None'}")
            self.console.print(f"  Priority: {current_task.priority.value}")
            self.console.print(f"  Tags: {', '.join(current_task.tags) if current_task.tags else 'None'}")

            # Get new values (with current values as defaults)
            new_title = Prompt.ask("[bold cyan]New title (leave blank to keep current)[/bold cyan]", default=current_task.title)
            if new_title == current_task.title:
                new_title = None  # Will be ignored in update call

            new_description = Prompt.ask("[bold cyan]New description (leave blank to keep current)[/bold cyan]", default=current_task.description or "")
            if new_description == (current_task.description or ""):
                new_description = None  # Will be ignored in update call

            priority_choice = Prompt.ask("[bold cyan]New priority ([blue]high[/blue]/[yellow]medium[/yellow]/[red]low[/red], leave blank to keep current)[/bold cyan]",
                                       choices=["high", "medium", "low", ""], default="")
            new_priority = Priority[priority_choice.upper()] if priority_choice else None

            tags_input = Prompt.ask("[bold cyan]New tags (comma-separated, leave blank to keep current)[/bold cyan]", default="")
            new_tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else None
            if tags_input == "":
                new_tags = None  # Will be ignored in update call

            # Perform update with only changed values
            updated_task = self.task_service.update_task(
                task_id=task_id,
                title=new_title,
                description=new_description,
                priority=new_priority,
                tags=new_tags
            )

            if updated_task:
                self.console.print(f"[green]✓ Task updated successfully[/green]")
            else:
                self.console.print(f"[red]Task with ID {task_id} not found.[/red]")

            self.console.input("\nPress Enter to return to main menu...")

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error updating task: {str(e)}[/red]")
            self.console.input("\nPress Enter to return to main menu...")

    def complete_task_action(self):
        """Action for completing a task"""
        self.console.clear()
        self.console.rule("[bold]Complete Task[/bold]")

        try:
            task_id = Prompt.ask("[bold cyan]Task ID to update[/bold cyan]")

            current_task = self.task_service.get_task(task_id)
            if not current_task:
                self.console.print(f"[red]Task with ID {task_id} not found.[/red]")
                self.console.input("\nPress Enter to return to main menu...")
                return

            current_status = "completed" if current_task.completed else "incomplete"
            new_status = Confirm.ask(f"Mark task as [bold]{'incomplete' if current_task.completed else 'complete'}[/bold]? (currently {current_status})")

            updated_task = self.task_service.complete_task(task_id, new_status)
            if updated_task:
                status_text = "completed" if new_status else "incomplete"
                self.console.print(f"[green]✓ Task marked as {status_text}[/green]")
            else:
                self.console.print(f"[red]Failed to update task status.[/red]")

            self.console.input("\nPress Enter to return to main menu...")

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error completing task: {str(e)}[/red]")
            self.console.input("\nPress Enter to return to main menu...")

    def delete_task_action(self):
        """Action for deleting a task"""
        self.console.clear()
        self.console.rule("[bold]Delete Task[/bold]")

        try:
            task_id = Prompt.ask("[bold cyan]Task ID to delete[/bold cyan]")

            confirm = Confirm.ask(f"[red]Are you sure you want to delete task {task_id}?[/red]")
            if not confirm:
                self.console.print("[yellow]Deletion cancelled.[/yellow]")
                self.console.input("\nPress Enter to return to main menu...")
                return

            success = self.task_service.delete_task(task_id)
            if success:
                self.console.print(f"[green]✓ Task deleted successfully[/green]")
            else:
                self.console.print(f"[red]Task with ID {task_id} not found.[/red]")

            self.console.input("\nPress Enter to return to main menu...")

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Error deleting task: {str(e)}[/red]")
            self.console.input("\nPress Enter to return to main menu...")

    def exit_action(self):
        """Action for exiting the application"""
        self.session_state.should_exit = True