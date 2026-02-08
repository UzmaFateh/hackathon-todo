from dataclasses import dataclass
from typing import Optional
from todo.interactive.menu import MenuState


@dataclass
class SessionState:
    menu_stack: list[MenuState] = None
    should_exit: bool = False
    task_service: Optional['TaskService'] = None

    def __post_init__(self):
        if self.menu_stack is None:
            self.menu_stack = []