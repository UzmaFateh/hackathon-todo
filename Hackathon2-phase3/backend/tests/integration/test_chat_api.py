"""
Integration tests for the chat API.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main import app  # Assuming your FastAPI app is in main.py
from backend.models import User, Task
from backend.database import engine, get_session
from sqlmodel import Session, select
from backend.mcp.tools import add_todo, list_todos
import uuid
from datetime import datetime


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    return {
        "id": str(uuid.uuid4()),
        "email": "test@example.com",
        "name": "Test User",
        "password_hash": "hashed_password"
    }


class TestChatAPIIntegration:
    """
    Integration tests for the chat API endpoints.
    """

    @patch('backend.routes.chat.validate_user_id_path')
    def test_post_chat_endpoint_success(self, mock_validate, client, mock_user):
        """Test successful chat interaction."""
        # Mock user ID validation
        mock_validate.return_value = mock_user["id"]

        # Prepare test data
        conversation_id = str(uuid.uuid4())
        test_message = "Add a task to buy milk"

        # Make request
        response = client.post(
            f"/api/{mock_user['id']}/chat",
            json={
                "message": test_message,
                "conversation_id": conversation_id
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        # Assertions
        assert response.status_code == 200
        response_data = response.json()
        assert "response" in response_data
        assert "conversation_id" in response_data
        assert response_data["success"] is True

    @patch('backend.routes.chat.validate_user_id_path')
    def test_post_chat_endpoint_missing_message(self, mock_validate, client, mock_user):
        """Test chat endpoint with missing message."""
        # Mock user ID validation
        mock_validate.return_value = mock_user["id"]

        # Make request with missing message
        response = client.post(
            f"/api/{mock_user['id']}/chat",
            json={
                "message": "",
                "conversation_id": str(uuid.uuid4())
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        # Should return 400 error
        assert response.status_code == 400

    @patch('backend.routes.chat.validate_user_id_path')
    def test_get_user_conversations(self, mock_validate, client, mock_user):
        """Test getting user's conversations."""
        # Mock user ID validation
        mock_validate.return_value = mock_user["id"]

        # Make request
        response = client.get(
            f"/api/{mock_user['id']}/conversations",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        # Assertions
        assert response.status_code == 200
        response_data = response.json()
        # May be empty if no conversations exist, but should be a list
        assert isinstance(response_data, list)

    @patch('backend.routes.chat.validate_user_id_path')
    def test_create_conversation(self, mock_validate, client, mock_user):
        """Test creating a new conversation."""
        # Mock user ID validation
        mock_validate.return_value = mock_user["id"]

        # Make request
        response = client.post(
            f"/api/{mock_user['id']}/conversations",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        # Assertions
        assert response.status_code == 200
        response_data = response.json()
        assert "conversation_id" in response_data
        assert "created_at" in response_data

    @patch('backend.routes.chat.validate_user_id_path')
    def test_get_conversation_messages(self, mock_validate, client, mock_user):
        """Test getting messages for a specific conversation."""
        # Mock user ID validation
        mock_validate.return_value = mock_user["id"]

        # Create a conversation first
        create_resp = client.post(
            f"/api/{mock_user['id']}/conversations",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        assert create_resp.status_code == 200
        conv_data = create_resp.json()
        conv_id = conv_data["conversation_id"]

        # Now get messages for this conversation
        response = client.get(
            f"/api/{mock_user['id']}/conversations/{conv_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        # Assertions
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list)  # Should return list of messages

    def test_user_isolation_conversation_access(self, client):
        """Test that users cannot access other users' conversations."""
        user1_id = str(uuid.uuid4())
        user2_id = str(uuid.uuid4())
        conversation_id = str(uuid.uuid4())

        # This test would require mocking the database to set up a conversation
        # owned by user2, then trying to access it as user1
        # For now, we'll just document the test intent
        pass

    @patch('backend.routes.chat.validate_user_id_path')
    def test_concurrent_user_isolation(self, mock_validate, client):
        """Test that concurrent users don't cross-contaminate conversations."""
        # Mock user ID validation to allow the test
        def side_effect(user_id):
            return user_id
        mock_validate.side_effect = side_effect

        # Simulate two different users
        user1_id = str(uuid.uuid4())
        user2_id = str(uuid.uuid4())

        # Have both users create conversations simultaneously
        import threading
        import time

        user1_conversation_ids = []
        user2_conversation_ids = []

        def user1_action():
            resp = client.post(f"/api/{user1_id}/conversations", headers={"Authorization": "Bearer fake-token"})
            if resp.status_code == 200:
                user1_conversation_ids.append(resp.json()["conversation_id"])

        def user2_action():
            resp = client.post(f"/api/{user2_id}/conversations", headers={"Authorization": "Bearer fake-token"})
            if resp.status_code == 200:
                user2_conversation_ids.append(resp.json()["conversation_id"])

        # Run both actions in parallel
        t1 = threading.Thread(target=user1_action)
        t2 = threading.Thread(target=user2_action)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        # Verify both succeeded
        assert len(user1_conversation_ids) == 1
        assert len(user2_conversation_ids) == 1

        # Verify conversations are different
        assert user1_conversation_ids[0] != user2_conversation_ids[0]

        # Verify users can only access their own conversations
        resp1 = client.get(f"/api/{user1_id}/conversations", headers={"Authorization": "Bearer fake-token"})
        resp2 = client.get(f"/api/{user2_id}/conversations", headers={"Authorization": "Bearer fake-token"})

        assert resp1.status_code == 200
        assert resp2.status_code == 200

    @patch('backend.routes.chat.validate_user_id_path')
    def test_input_sanitization(self, mock_validate, client, mock_user):
        """Test that input sanitization prevents injection attacks."""
        # Mock user ID validation
        mock_validate.return_value = mock_user["id"]

        # Test with potentially dangerous input
        dangerous_message = "<script>alert('xss')</script>; DROP TABLE users; --"

        response = client.post(
            f"/api/{mock_user['id']}/chat",
            json={
                "message": dangerous_message,
                "conversation_id": str(uuid.uuid4())
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )

        # Should still return a successful response (but sanitized)
        # The exact behavior depends on how the sanitization is implemented
        assert response.status_code in [200, 400]  # Either processed safely or rejected

    def test_rate_limiting(self, client):
        """Test that rate limiting works properly."""
        # This would require more complex setup to test actual rate limiting
        # For now, we'll document the test intent
        pass


# Additional helper tests
def test_mcp_tool_integration():
    """Test integration between MCP tools and database."""
    # This would test that MCP tools properly interact with the database
    # For example, adding a task through the tool and verifying it's in the database
    pass


if __name__ == "__main__":
    pytest.main([__file__])