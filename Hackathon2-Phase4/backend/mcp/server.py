import asyncio
from mcp.server import Server
from mcp.types import TextContent, Resource, Diagnostic
from pydantic import AnyUrl
from typing import List, Dict, Any
import logging

# Import the tools we need to register
from backend.mcp.tools import add_todo, list_todos, update_todo, complete_todo, delete_todo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global server instance
server = Server("todo-mcp-server")


async def handle_initialization(context):
    """
    Handle MCP server initialization.
    """
    logger.info("MCP Server initialized")
    return {
        "server_info": {
            "name": "todo-mcp-server",
            "version": "1.0.0"
        },
        "capabilities": {
            "tools": {}
        }
    }


def setup_mcp_server():
    """
    Set up the MCP server with proper initialization and tool registration.
    """
    logger.info("Setting up MCP server...")

    # Register initialization handler
    server.on_initialize(handle_initialization)

    # Register the todo tools using mcp-todo-skill patterns
    @server.request("tools/list")
    async def list_tools(request) -> Dict[str, Any]:
        """List available tools."""
        return {
            "tools": [
                {
                    "name": "add_todo",
                    "description": "Add a new task to the user's todo list"
                },
                {
                    "name": "list_todos",
                    "description": "List all tasks in the user's todo list, with options to filter by status"
                },
                {
                    "name": "update_todo",
                    "description": "Update an existing task in the user's todo list"
                },
                {
                    "name": "complete_todo",
                    "description": "Mark a task as completed"
                },
                {
                    "name": "delete_todo",
                    "description": "Delete a task from the user's todo list"
                }
            ]
        }

    # Register add_todo tool
    @server.request("tools/call")
    async def handle_add_todo(request) -> Dict[str, Any]:
        """Handle add_todo tool calls."""
        try:
            params = request.get("arguments", {})
            result = add_todo(
                title=params.get("title", ""),
                description=params.get("description", ""),
                user_id=params.get("user_id")
            )
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in add_todo: {str(e)}")
            return {"error": str(e)}

    # Register list_todos tool
    @server.request("tools/call")
    async def handle_list_todos(request) -> Dict[str, Any]:
        """Handle list_todos tool calls."""
        try:
            params = request.get("arguments", {})
            result = list_todos(
                user_id=params.get("user_id"),
                status=params.get("status", "all")
            )
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in list_todos: {str(e)}")
            return {"error": str(e)}

    # Register update_todo tool
    @server.request("tools/call")
    async def handle_update_todo(request) -> Dict[str, Any]:
        """Handle update_todo tool calls."""
        try:
            params = request.get("arguments", {})
            result = update_todo(
                task_id=params.get("task_id"),
                user_id=params.get("user_id"),
                title=params.get("title"),
                is_completed=params.get("is_completed")
            )
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in update_todo: {str(e)}")
            return {"error": str(e)}

    # Register complete_todo tool
    @server.request("tools/call")
    async def handle_complete_todo(request) -> Dict[str, Any]:
        """Handle complete_todo tool calls."""
        try:
            params = request.get("arguments", {})
            result = complete_todo(
                task_id=params.get("task_id"),
                user_id=params.get("user_id")
            )
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in complete_todo: {str(e)}")
            return {"error": str(e)}

    # Register delete_todo tool
    @server.request("tools/call")
    async def handle_delete_todo(request) -> Dict[str, Any]:
        """Handle delete_todo tool calls."""
        try:
            params = request.get("arguments", {})
            result = delete_todo(
                task_id=params.get("task_id"),
                user_id=params.get("user_id")
            )
            return {"result": result}
        except Exception as e:
            logger.error(f"Error in delete_todo: {str(e)}")
            return {"error": str(e)}

    logger.info("MCP server setup complete with all tools registered")
    return server


async def run_server():
    """
    Run the MCP server over stdio.
    """
    mcp_server = setup_mcp_server()

    async with mcp_server.serve_over_stdio():
        logger.info("MCP server running over stdio...")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(run_server())