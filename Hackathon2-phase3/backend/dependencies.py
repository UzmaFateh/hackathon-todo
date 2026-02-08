from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlmodel import Session
from db import engine
import uuid


def get_db_session():
    """
    Get database session dependency for FastAPI endpoints.

    Yields:
        Session: Database session for the request
    """
    with Session(engine) as session:
        yield session


# Database session dependency
DBSessionDep = Annotated[Session, Depends(get_db_session)]


def validate_user_id_path(user_id: str) -> str:
    """
    Validate that the user_id in the path is a valid UUID.

    Args:
        user_id: User ID from path parameter

    Returns:
        str: Validated user ID

    Raises:
        HTTPException: If user_id is not a valid UUID
    """
    try:
        uuid.UUID(user_id)
        return user_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )


def validate_conversation_id_path(conversation_id: str) -> str:
    """
    Validate that the conversation_id in the path is a valid UUID.

    Args:
        conversation_id: Conversation ID from path parameter

    Returns:
        str: Validated conversation ID

    Raises:
        HTTPException: If conversation_id is not a valid UUID
    """
    try:
        uuid.UUID(conversation_id)
        return conversation_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )


# For JWT authentication, we'll use the Better Auth integration
# The actual JWT validation will be handled by the Better Auth middleware
# These functions provide path validation and session management