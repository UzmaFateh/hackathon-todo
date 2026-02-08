import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
from contextlib import contextmanager

logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Use synchronization engine for simplicity in Phase II foundation as SQLModel
# has better support for it, but we can transition to async later if needed.
# Neon supports both.
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """Initialize the database with all table schemas."""
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    """Get a database session for use with FastAPI dependencies."""
    with Session(engine) as session:
        yield session


def get_transactional_session():
    """Get a database session that ensures ACID compliance with proper rollback."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database transaction rolled back due to error: {str(e)}")
            raise


def execute_in_transaction(operation_func, *args, **kwargs):
    """
    Execute a function within a database transaction with ACID compliance.

    Args:
        operation_func: Function to execute within transaction
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Result of the operation function
    """
    with Session(engine) as session:
        try:
            result = operation_func(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            logger.error(f"Transaction failed and was rolled back: {str(e)}")
            raise


# Engine available globally for direct access when needed
__all__ = ["engine", "init_db", "get_session", "get_transactional_session", "execute_in_transaction"]
