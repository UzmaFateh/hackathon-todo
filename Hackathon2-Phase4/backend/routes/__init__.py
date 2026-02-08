"""Routes package for API endpoints."""

from . import auth
from . import chat
from . import tasks
from . import tags

__all__ = ["auth", "chat", "tasks", "tags"]
