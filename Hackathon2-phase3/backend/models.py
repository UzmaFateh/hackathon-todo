from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


class User(SQLModel, table=True):
    """
    User model representing registered users in the system.
    Each user can only access their own tasks due to user isolation.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str = Field(default="")
    password_hash: str  # Hashed password stored securely
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks - each user has many tasks
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)
    # Relationship to conversations - each user has many conversations
    conversations: List["Conversation"] = Relationship(back_populates="user", cascade_delete=True)


class Task(SQLModel, table=True):
    """
    Task model representing todo items.
    Each task belongs to a single user and can only be accessed by that user.
    The user_id foreign key enforces user isolation at the database level.
    """
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)  # Enforces user isolation
    title: str = Field(max_length=255, default="Untitled Task")
    is_completed: bool = Field(default=False)
    priority: str = Field(default="medium")  # Task priority: high, medium, low
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional[User] = Relationship(back_populates="tasks")

    # Relationship to tag assignments (many-to-many through TaskTagAssignment)
    tag_assignments: List["TaskTagAssignment"] = Relationship(back_populates="task", cascade_delete=True)

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session between user and AI agent.
    Each conversation belongs to a single user and can only be accessed by that user.
    The user_id foreign key enforces user isolation at the database level.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)  # Enforces user isolation
    title: Optional[str] = Field(default=None, max_length=200, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional[User] = Relationship(back_populates="conversations")
    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)

    def handle_concurrent_access_conflict(self, other_conversation) -> bool:
        """
        Handle conflicts that may arise from concurrent access to the same conversation.

        Args:
            other_conversation: Another conversation instance to compare with

        Returns:
            True if conflict was resolved, False otherwise
        """
        # For now, this is a simple check to ensure consistency
        # In a real implementation, you might want to implement more sophisticated
        # conflict resolution strategies like last-write-wins or merge strategies
        return self.updated_at != other_conversation.updated_at


class Message(SQLModel, table=True):
    """
    Message model representing individual exchanges in a conversation.
    Each message belongs to a single conversation and is isolated by user context.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", index=True)
    role: str = Field(regex="^(user|assistant)$")  # Enum-like validation
    content: str = Field(max_length=10000)
    sequence_number: int = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")


class TaskTag(SQLModel, table=True):
    """
    Tag model for categorizing tasks.
    Each tag is scoped to a user - users have their own tag namespace.
    Tags are automatically deleted when no tasks reference them (via database trigger).
    """
    __tablename__ = "task_tags"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)  # User isolation
    name: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tag assignments (many-to-many through TaskTagAssignment)
    tag_assignments: List["TaskTagAssignment"] = Relationship(back_populates="tag", cascade_delete=True)


class TaskTagAssignment(SQLModel, table=True):
    """
    Junction table for many-to-many relationship between Tasks and TaskTags.
    Allows a task to have multiple tags and a tag to be assigned to multiple tasks.
    """
    __tablename__ = "task_tag_assignments"

    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="task_tags.id", primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: Optional[Task] = Relationship(back_populates="tag_assignments")
    tag: Optional[TaskTag] = Relationship(back_populates="tag_assignments")
