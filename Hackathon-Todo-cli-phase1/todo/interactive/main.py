import sys
from rich.console import Console
from rich.prompt import Prompt
from todo.services.task_service import TaskService
from todo.repositories.in_memory_repo import InMemoryTaskRepository
from todo.interactive.session import SessionState
from todo.interactive.controllers import MenuController


class InteractiveTodoApp:
    def __init__(self):
        # Initialize the repository and service (shared with existing CLI)
        self.repository = InMemoryTaskRepository()
        self.task_service = TaskService(self.repository)

        # Initialize session state with the task service
        self.session_state = SessionState(
            task_service=self.task_service
        )

        self.console = Console()
        self.controller = MenuController(self.session_state)

    def run(self):
        """Run the interactive menu application in a continuous loop"""
        self.console.print("[bold green]Welcome to the Interactive Todo App![/bold green]")
        self.console.print("Use the menu to manage your tasks.\n")

        while not self.session_state.should_exit:
            try:
                # Display the main menu
                self.controller.display_main_menu()

                # Get user choice
                choice = Prompt.ask(
                    "\n[bold cyan]Select an option (1-6) or 'q' to quit[/bold cyan]",
                    choices=[str(i) for i in range(1, 7)] + ['q'],
                    default="1"
                )

                if choice.lower() == 'q':
                    self.session_state.should_exit = True
                    break

                # Convert choice to integer and get the corresponding menu item
                choice_idx = int(choice) - 1
                menu_items = self.controller.get_main_menu_items()

                if 0 <= choice_idx < len(menu_items):
                    menu_item = menu_items[choice_idx]
                    menu_item.action()
                else:
                    self.console.print("[red]Invalid selection. Please try again.[/red]")

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Exiting...[/yellow]")
                self.session_state.should_exit = True
            except Exception as e:
                self.console.print(f"[red]An error occurred: {str(e)}[/red]")
                self.console.input("Press Enter to continue...")

        self.console.print("[bold blue]Thanks for using the Interactive Todo App![/bold blue]")


def main():
    """Main entry point for the interactive CLI"""
    app = InteractiveTodoApp()
    app.run()


if __name__ == "__main__":
    main()