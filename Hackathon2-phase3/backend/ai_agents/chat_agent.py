"""
Chat Agent implementation with Gemini backend via OpenAI-compatible API.

This agent processes user messages and coordinates with MCP tools for todo management.
"""
import os
import logging
import functools
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv, find_dotenv

# Import OpenAI Agents SDK
from agents import Agent, Runner, AsyncOpenAI, ModelSettings, OpenAIChatCompletionsModel, function_tool

# Import MCP tools
from mcp.tools import add_todo, list_todos, update_todo, complete_todo, delete_todo

# Load environment variables
load_dotenv(find_dotenv())

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
# Ensure OPENAI_API_KEY is set (even if dummy for Gemini)
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "dummy-key-for-gemini"

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

if not gemini_api_key:
    logger.warning("Warning: GEMINI_API_KEY not found in .env")

# Initialize the client once
# 1. Which LLM Service? (Gemini via OpenAI-compatible API)
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=external_client
)

def create_chat_agent(user_id: str, model_name: str = "gemini-2.5-flash-lite") -> Agent:
    """
    Create and return a configured chat agent with user-bound tools.
    
    Args:
        user_id: User ID for the agent to bind tools to
        model_name: Name of the Gemini/Gemma model to use
        
    Returns:
        Configured Agent instance
    """
    try:
        # Initialize the model dynamically
        current_llm_model = OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=external_client
        )
        # Create partial functions for tools with user_id bound
        # We need to wrap them to preserve metadata for the agent SDK
        
        @function_tool
        def add_task(title: str, description: str = None, priority: str = "medium") -> str:
            """
            Add a new task/todo.
            
            Args:
                title: Title of the task
                description: Optional description
                priority: Task priority (high, medium, low)
            """
            result = add_todo(title=title, user_id=user_id, description=description, priority=priority)
            if result.get("success"):
                task = result.get("task", {})
                return f"Task added successfully: ID={task.get('id')}, Title='{task.get('title')}'"
            else:
                return f"Failed to add task: {result.get('error')}"

        @function_tool
        def list_tasks(status: str = "all") -> str:
            """
            List tasks/todos.
            
            Args:
                status: Filter status ("all", "pending", "completed")
            """
            try:
                result = list_todos(user_id=user_id, status=status)
                print(f"[DEBUG] list_todos result: {result}")
                if result.get("success"):
                    tasks = result.get("tasks", [])
                    if not tasks:
                        return "You have no tasks."
                    
                    task_list = []
                    for t in tasks:
                        status_str = "[x]" if t['completed'] else "[ ]"
                        task_list.append(f"{t['id']}. {status_str} {t['title']} ({t['priority']})")
                    return "\n".join(task_list)
                else:
                    error_msg = f"Failed to list tasks: {result.get('error')}"
                    print(f"[DEBUG] Returning error: {error_msg}")
                    return error_msg
            except Exception as e:
                import traceback
                traceback.print_exc()
                return f"Error listing tasks: {str(e)}"

        @function_tool
        def update_task(task_id: int, title: str = None, priority: str = None) -> str:
            """
            Update a task/todo.
            
            Args:
                task_id: ID of the task to update
                title: New title (optional)
                priority: New priority (optional)
            """
            result = update_todo(task_id=task_id, user_id=user_id, title=title, priority=priority)
            if result.get("success"):
                task = result.get("task", {})
                return f"Task updated successfully: {task.get('title')}"
            else:
                return f"Failed to update task: {result.get('error')}"

        @function_tool
        def complete_task(task_id: int) -> str:
            """
            Mark a task/todo as complete.
            
            Args:
                task_id: ID of the task to complete
            """
            result = complete_todo(task_id=task_id, user_id=user_id)
            if result.get("success"):
                task = result.get("task", {})
                return f"Task marked as completed: {task.get('title')}"
            else:
                return f"Failed to complete task: {result.get('error')}"

        @function_tool
        def delete_task(task_id: int) -> str:
            """
            Delete a task/todo.
            
            Args:
                task_id: ID of the task to delete
            """
            result = delete_todo(task_id=task_id, user_id=user_id)
            if result.get("success"):
                return "Task deleted successfully"
            else:
                return f"Failed to delete task: {result.get('error')}"

        # Create the agent
        agent = Agent(
            name="TodoAssistant",
            instructions="""You are a helpful Todo AI Assistant. 
            You help users manage their tasks using the provided tools.
            Always be friendly and concise.
            If a user asks to add a task, use add_task.
            If a user asks to list tasks, use list_tasks.
            If a user asks to complete a task, use complete_task.
            If a user asks to delete a task, use delete_task.
            If a user asks to update a task, use update_task.
            When listing tasks, present them in a clean, readable format.
            """,
            model=current_llm_model,
            tools=[add_task, list_tasks, update_task, complete_task, delete_task],
        )
        
        return agent
        
    except Exception as e:
        logger.error(f"Error creating chat agent: {str(e)}")
        raise


class ChatAgentRunner:
    """Runner for the chat agent."""
    
    @staticmethod
    async def process_message(agent: Agent, message: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Process a message with the agent.
        
        Args:
            agent: The configured Agent instance
            message: User's message
            history: Conversation history (optional)
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Construct context from history if provided
            full_message = message
            if history:
                # Take last 6 messages (3 turns) for context
                context_parts = []
                for msg in history[-6:]:
                    role = "User" if msg['role'] == 'user' else "Assistant"
                    context_parts.append(f"{role}: {msg['content']}")
                
                context_str = "\n".join(context_parts)
                full_message = f"Previous conversation context:\n{context_str}\n\nCurrent User Message: {message}"
                logger.info(f"Running agent with context from {len(history)} previous messages")

            # Run the agent
            result = await Runner.run(agent, full_message)
            
            return {
                "response": result.final_output,
                "task_operations": [],
                "metadata": {"model": "gemini-2.5-flash", "provider": "google", "context_included": bool(history)}
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "response": f"I encountered an error: {str(e)}",
                "task_operations": [],
                "metadata": {"error": str(e)}
            }
