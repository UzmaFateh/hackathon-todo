from dataclasses import dataclass
from typing import Callable, Optional
from rich.panel import Panel
from rich.table import Table
from rich.console import Console


@dataclass
class MenuItem:
    id: str
    title: str
    description: str
    action: Callable[[], None]
    hotkey: Optional[str] = None


@dataclass
class MenuState:
    current_selection: int = 0
    items: list[MenuItem] = None
    title: str = "Todo App Menu"

    def __post_init__(self):
        if self.items is None:
            self.items = []