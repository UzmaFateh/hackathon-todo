from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    id: str
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    tags: List[str] = None
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class TaskFilter:
    status: Optional[str] = None
    priority: Optional[Priority] = None
    search_term: Optional[str] = None
    tags: Optional[List[str]] = None