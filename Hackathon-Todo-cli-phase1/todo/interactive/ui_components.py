from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.style import Style


class UIComponents:
    """Collection of reusable UI components for the interactive menu"""

    def __init__(self):
        self.console = Console()

    def create_styled_table(self, title: str = None, headers: list = None) -> Table:
        """Create a styled table with optional title and headers"""
        table = Table(title=title, title_style="bold blue", header_style="bold cyan")

        if headers:
            for header in headers:
                table.add_column(header)
        else:
            table.add_column("Item", style="cyan")
            table.add_column("Value", style="white")

        return table

    def create_styled_panel(self, content: str, title: str = None, style: str = "blue") -> Panel:
        """Create a styled panel with content and optional title"""
        return Panel(content, title=title, border_style=style, padding=(1, 2))

    def create_colored_text(self, text: str, style: str = "white") -> Text:
        """Create colored text with specified style"""
        return Text(text, style=style)

    def show_message(self, message: str, style: str = "white"):
        """Display a styled message"""
        self.console.print(Text(message, style=style))

    def show_success(self, message: str):
        """Display a success message"""
        self.console.print(Text(message, style="green bold"))

    def show_error(self, message: str):
        """Display an error message"""
        self.console.print(Text(message, style="red bold"))

    def show_warning(self, message: str):
        """Display a warning message"""
        self.console.print(Text(message, style="yellow bold"))

    def show_info(self, message: str):
        """Display an info message"""
        self.console.print(Text(message, style="blue bold"))

    def get_user_input(self, prompt: str, default: str = None) -> str:
        """Get user input with styled prompt"""
        return Prompt.ask(f"[bold]{prompt}[/bold]", default=default)

    def get_confirmation(self, prompt: str) -> bool:
        """Get yes/no confirmation from user"""
        return Confirm.ask(f"[bold]{prompt}[/bold]")