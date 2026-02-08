"""
Unit tests for MCP tools.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.mcp.tools import TodoMCPTools, add_todo, list_todos, update_todo, complete_todo, delete_todo
from backend.models import Task, User
from backend.database import engine
from sqlmodel import Session, create_engine
from uuid import UUID
import uuid


class TestTodoMCPTools:
    """
    Unit tests for the TodoMCPTools class and individual functions.
    """

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.tools = TodoMCPTools()

        # Create a mock user ID for testing
        self.mock_user_id = str(uuid.uuid4())
        self.mock_user = User(
            id=self.mock_user_id,
            email="test@example.com",
            name="Test User",
            password_hash="hashed_password"
        )

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_add_todo_success(self, mock_engine, mock_session_class):
        """Test successful addition of a todo."""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock user exists
        mock_session.get.return_value = self.mock_user

        # Mock task creation
        mock_task = Task(
            id=1,
            user_id=self.mock_user_id,
            title="Test Task",
            is_completed=False,
            priority="medium"
        )
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Call the function
        result = add_todo("Test Task", "Test Description", self.mock_user_id)

        # Assertions
        assert result["success"] is True
        assert result["task_id"] is not None
        assert "Successfully added task" in result["message"]

        # Verify session methods were called
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_add_todo_missing_title(self, mock_engine, mock_session_class):
        """Test add_todo with missing title."""
        result = add_todo("", "Test Description", self.mock_user_id)

        assert result["success"] is False
        assert result["error_code"] == "MISSING_TITLE"

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_add_todo_missing_user_id(self, mock_engine, mock_session_class):
        """Test add_todo with missing user ID."""
        result = add_todo("Test Task", "Test Description", "")

        assert result["success"] is False
        assert result["error_code"] == "MISSING_USER_ID"

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_add_todo_invalid_user_id(self, mock_engine, mock_session_class):
        """Test add_todo with invalid user ID."""
        result = add_todo("Test Task", "Test Description", "invalid-uuid")

        assert result["success"] is False
        assert result["error_code"] == "INVALID_USER_ID"

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_add_todo_user_not_found(self, mock_engine, mock_session_class):
        """Test add_todo when user doesn't exist."""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock user doesn't exist
        mock_session.get.return_value = None

        result = add_todo("Test Task", "Test Description", self.mock_user_id)

        assert result["success"] is False
        assert result["error_code"] == "USER_NOT_FOUND"

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_list_todos_success(self, mock_engine, mock_session_class):
        """Test successful listing of todos."""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock user exists
        mock_session.get.return_value = self.mock_user

        # Mock tasks
        mock_tasks = [
            Task(
                id=1,
                user_id=self.mock_user_id,
                title="Task 1",
                is_completed=False,
                priority="high"
            ),
            Task(
                id=2,
                user_id=self.mock_user_id,
                title="Task 2",
                is_completed=True,
                priority="low"
            )
        ]
        mock_exec_result = Mock()
        mock_exec_result.all.return_value = mock_tasks
        mock_session.exec.return_value = mock_exec_result

        result = list_todos(self.mock_user_id)

        assert result["success"] is True
        assert len(result["tasks"]) == 2
        assert result["count"] == 2

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_list_todos_empty(self, mock_engine, mock_session_class):
        """Test listing todos when none exist."""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock user exists
        mock_session.get.return_value = self.mock_user

        # Mock empty tasks
        mock_exec_result = Mock()
        mock_exec_result.all.return_value = []
        mock_session.exec.return_value = mock_exec_result

        result = list_todos(self.mock_user_id)

        assert result["success"] is True
        assert len(result["tasks"]) == 0
        assert result["count"] == 0

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_update_todo_success(self, mock_engine, mock_session_class):
        """Test successful updating of a todo."""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock user and task exist
        mock_session.get.side_effect = [self.mock_user, Task(
            id=1,
            user_id=self.mock_user_id,
            title="Old Title",
            is_completed=False,
            priority="medium"
        )]

        result = update_todo(1, self.mock_user_id, title="New Title")

        assert result["success"] is True
        assert "Task updated successfully" in result["message"]
        assert result["task"]["title"] == "New Title"

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_update_todo_access_denied(self, mock_engine, mock_session_class):
        """Test updating a todo that doesn't belong to the user."""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock user exists but task belongs to different user
        mock_session.get.side_effect = [self.mock_user, Task(
            id=1,
            user_id=str(uuid.uuid4()),  # Different user
            title="Old Title",
            is_completed=False,
            priority="medium"
        )]

        result = update_todo(1, self.mock_user_id, title="New Title")

        assert result["success"] is False
        assert result["error_code"] == "ACCESS_DENIED"

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_complete_todo_success(self, mock_engine, mock_session_class):
        """Test successful completion of a todo."""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock user and task exist
        mock_session.get.side_effect = [self.mock_user, Task(
            id=1,
            user_id=self.mock_user_id,
            title="Test Task",
            is_completed=False,
            priority="medium"
        )]

        result = complete_todo(1, self.mock_user_id)

        assert result["success"] is True
        assert "Task updated successfully" in result["message"]
        assert result["task"]["is_completed"] is True

    @patch('backend.mcp.tools.Session')
    @patch('backend.mcp.tools.engine')
    def test_delete_todo_success(self, mock_engine, mock_session_class):
        """Test successful deletion of a todo."""
        # Mock session
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        # Mock user and task exist
        mock_session.get.side_effect = [self.mock_user, Task(
            id=1,
            user_id=self.mock_user_id,
            title="Test Task",
            is_completed=False,
            priority="medium"
        )]

        result = delete_todo(1, self.mock_user_id)

        assert result["success"] is True
        assert "Task deleted successfully" in result["message"]

        # Verify delete was called
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_invalid_uuid_handling(self):
        """Test that invalid UUIDs are properly handled."""
        result = add_todo("Test", "Desc", "not-a-valid-uuid")
        assert result["success"] is False
        assert result["error_code"] == "INVALID_USER_ID"


# Run tests if this file is executed directly
if __name__ == "__main__":
    pytest.main([__file__])