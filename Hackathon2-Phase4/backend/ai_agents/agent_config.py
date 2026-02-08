"""
Configuration for the AI Todo Chatbot agent using OpenAI Agents SDK with Gemini backend.

This module defines the agent's instructions, tool configurations, and behavior patterns
for interacting with users in a natural language conversation about todo management.
"""

from typing import Dict, Any, List
from enum import Enum


class AgentPersona(Enum):
    HELPFUL_ASSISTANT = "helpful_assistant"
    PRODUCTIVITY_COACH = "productivity_coach"
    TASK_MANAGER = "task_manager"


# Main agent instructions - defines the AI's behavior and response patterns
AGENT_INSTRUCTIONS = """
You are an AI productivity assistant that helps users manage their tasks through natural language conversation.
Your primary function is to assist users with adding, listing, updating, completing, and deleting tasks.
You must use the provided tools to interact with the task system.
Always be helpful, friendly, and concise in your responses.
If you're uncertain about a user's request, ask clarifying questions.
Never make up information or task IDs - only use data returned by the tools.
If a tool fails, inform the user politely and suggest alternatives.
Keep responses focused on task management functionality.
You are using the openai-agents-gemini skill to interact with the system.
Follow the Gemini-specific patterns for tool usage and response formatting.
Always ensure user data privacy and security.
"""


# Tool descriptions for the agent compatible with openai-agents-gemini skill
TOOL_DESCRIPTIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_todo",
            "description": "Add a new task to the user's todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task to add"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user (provided automatically)"
                    }
                },
                "required": ["title", "user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_todos",
            "description": "List all tasks in the user's todo list, with options to filter by status",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user (provided automatically)"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status (default: all)"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_todo",
            "description": "Update an existing task in the user's todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user (provided automatically)"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task (optional)"
                    },
                    "is_completed": {
                        "type": "boolean",
                        "description": "Whether the task is completed (optional)"
                    }
                },
                "required": ["task_id", "user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_todo",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to mark as completed"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user (provided automatically)"
                    }
                },
                "required": ["task_id", "user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_todo",
            "description": "Delete a task from the user's todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user (provided automatically)"
                    }
                },
                "required": ["task_id", "user_id"]
            }
        }
    }
]


# Error handling configuration
ERROR_HANDLING_CONFIG = {
    "max_retries": 3,
    "retry_delay": 1.0,
    "friendly_error_prefix": "I encountered an issue",
    "fallback_suggestions": [
        "Please try rephrasing your request",
        "Check that your request includes all necessary details",
        "Try breaking your request into smaller steps"
    ]
}


# Response formatting configuration
RESPONSE_FORMATTING_CONFIG = {
    "max_response_tokens": 500,
    "temperature": 0.7,
    "top_p": 0.9,
    "presence_penalty": 0.1,
    "frequency_penalty": 0.1
}


# Conversation context management
CONVERSATION_CONTEXT_CONFIG = {
    "max_history_length": 10,
    "summary_threshold": 20,
    "context_retention_rate": 0.8
}


# Default agent configuration
DEFAULT_AGENT_CONFIG: Dict[str, Any] = {
    "instructions": AGENT_INSTRUCTIONS,
    "tools": TOOL_DESCRIPTIONS,  # Using the properly formatted tool descriptions
    "model": "gemini-pro",  # Using gemini backend via openai-agents-gemini skill
    "temperature": RESPONSE_FORMATTING_CONFIG["temperature"],
    "top_p": RESPONSE_FORMATTING_CONFIG["top_p"],
    "max_completion_tokens": RESPONSE_FORMATTING_CONFIG["max_response_tokens"],
    "tool_choice": "auto"
}


def get_agent_config(persona: AgentPersona = AgentPersona.HELPFUL_ASSISTANT) -> Dict[str, Any]:
    """
    Get agent configuration based on selected persona.

    Args:
        persona: The agent persona to use

    Returns:
        Dictionary containing the agent configuration
    """
    base_config = DEFAULT_AGENT_CONFIG.copy()

    # Customize instructions based on persona
    if persona == AgentPersona.PRODUCTIVITY_COACH:
        base_config["instructions"] = AGENT_INSTRUCTIONS.replace(
            "You are an AI productivity assistant",
            "You are an AI productivity coach"
        ).replace(
            "assist users with adding, listing, updating, completing, and deleting tasks",
            "coach users to better manage their tasks and improve productivity"
        )
    elif persona == AgentPersona.TASK_MANAGER:
        base_config["instructions"] = AGENT_INSTRUCTIONS.replace(
            "You are an AI productivity assistant",
            "You are an AI task manager"
        ).replace(
            "assist users with adding, listing, updating, completing, and deleting tasks",
            "manage user tasks efficiently and effectively"
        )

    return base_config


# Export the main configuration
__all__ = [
    "AGENT_INSTRUCTIONS",
    "TOOL_DESCRIPTIONS",
    "ERROR_HANDLING_CONFIG",
    "RESPONSE_FORMATTING_CONFIG",
    "CONVERSATION_CONTEXT_CONFIG",
    "DEFAULT_AGENT_CONFIG",
    "get_agent_config",
    "AgentPersona"
]