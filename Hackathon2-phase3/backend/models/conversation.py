from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200, nullable=True)


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a chat session between user and AI agent.
    Each conversation belongs to a single user and can only be accessed by that user.
    The user_id foreign key enforces user isolation at the database level.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)  # Enforces user isolation
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)


# Need to import Message after defining Conversation to avoid circular import issues
# We'll define the Message model in a separate file and import it here if needed
# For now, we'll use string annotation for the back_populates reference