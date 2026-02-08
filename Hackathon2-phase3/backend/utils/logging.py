"""
Comprehensive logging utility for chat operations.
"""
import logging
import sys
from typing import Any, Dict
from datetime import datetime
import json


class ChatLogger:
    """
    Comprehensive logger for chat operations with structured logging.
    """

    def __init__(self, name: str = "chat_logger", level: int = logging.INFO):
        """
        Initialize the chat logger.

        Args:
            name: Name of the logger
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent adding multiple handlers if logger already exists
        if not self.logger.handlers:
            # Create console handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)

            # Create formatter with more detailed information
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)

            # Add handler to logger
            self.logger.addHandler(handler)

    def log_chat_start(self, user_id: str, conversation_id: str):
        """
        Log the start of a chat conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
        """
        self.logger.info(f"Chat started - User: {user_id}, Conversation: {conversation_id}")

    def log_user_message(self, user_id: str, conversation_id: str, message: str):
        """
        Log a user message.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            message: The message content
        """
        self.logger.info(f"User message - User: {user_id}, Conversation: {conversation_id}, Message: {message[:50]}...")

    def log_agent_response(self, user_id: str, conversation_id: str, response: str):
        """
        Log an agent response.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            response: The agent's response
        """
        self.logger.info(f"Agent response - User: {user_id}, Conversation: {conversation_id}, Response: {response[:50]}...")

    def log_tool_execution(self, user_id: str, conversation_id: str, tool_name: str, params: Dict[str, Any]):
        """
        Log tool execution.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            tool_name: The name of the tool executed
            params: Parameters passed to the tool
        """
        self.logger.info(f"Tool executed - User: {user_id}, Conversation: {conversation_id}, Tool: {tool_name}, Params: {params}")

    def log_error(self, user_id: str, conversation_id: str, error: Exception, context: str = ""):
        """
        Log an error.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            error: The error that occurred
            context: Additional context about the error
        """
        self.logger.error(f"Error in chat - User: {user_id}, Conversation: {conversation_id}, Context: {context}, Error: {str(error)}", exc_info=True)

    def log_chat_end(self, user_id: str, conversation_id: str):
        """
        Log the end of a chat conversation.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
        """
        self.logger.info(f"Chat ended - User: {user_id}, Conversation: {conversation_id}")


# Global logger instance
chat_logger = ChatLogger()


def get_chat_logger() -> ChatLogger:
    """
    Get the global chat logger instance.

    Returns:
        ChatLogger instance
    """
    return chat_logger