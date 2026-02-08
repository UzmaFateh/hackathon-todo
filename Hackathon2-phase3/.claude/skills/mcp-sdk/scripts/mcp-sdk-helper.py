#!/usr/bin/env python3
"""
MCP SDK Helper Script

This script provides common operations for working with the Model Context Protocol (MCP) Python SDK.
"""

import argparse
import asyncio
from mcp.server.fastmcp import FastMCP


def create_demo_server(name: str = "Demo Server", transport: str = "stdio", port: int = 3000):
    """Create a demo MCP server with sample tools."""

    mcp = FastMCP(name, json_response=True)

    @mcp.tool()
    def add(a: int, b: int) -> int:
        """Add two numbers together."""
        return a + b

    @mcp.tool()
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers together."""
        return a * b

    @mcp.tool()
    def greet(name: str, greeting: str = "Hello") -> str:
        """Create a personalized greeting."""
        return f"{greeting}, {name}! Welcome to MCP."

    @mcp.resource(f"greeting://{name}")
    def get_greeting(name: str) -> str:
        """Get a personalized greeting resource."""
        return f"Hello, {name}!"

    @mcp.prompt()
    def create_welcome_message(name: str, style: str = "friendly") -> str:
        """Generate a welcome message with specified style."""
        styles = {
            "friendly": "Please write a warm, friendly welcome message",
            "formal": "Please write a formal, professional welcome message",
            "casual": "Please write a casual, relaxed welcome message",
        }
        return f"{styles.get(style, styles['friendly'])} for {name}."

    return mcp


def run_server(name: str, transport: str, port: int):
    """Run an MCP server with specified parameters."""
    print(f"Starting MCP server '{name}' with {transport} transport on port {port}...")

    mcp = create_demo_server(name, transport, port)

    try:
        if transport == "streamable-http":
            mcp.run(transport="streamable-http", port=port)
        elif transport == "stdio":
            mcp.run(transport="stdio")
        elif transport == "sse":
            mcp.run(transport="sse")
        else:
            print(f"Unsupported transport: {transport}")
            print("Supported transports: streamable-http, stdio, sse")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error running server: {e}")


async def run_async_example():
    """Demonstrate async capabilities."""
    print("Async example would run here.")
    # This would typically connect to a running server and make async calls


def main():
    parser = argparse.ArgumentParser(description="MCP SDK Helper")
    parser.add_argument("--action", choices=["run-server", "async-example"], required=True,
                        help="Action to perform")
    parser.add_argument("--name", default="Demo Server", help="Name of the server")
    parser.add_argument("--transport", choices=["stdio", "streamable-http", "sse"],
                        default="stdio", help="Transport method")
    parser.add_argument("--port", type=int, default=3000, help="Port for HTTP transport")

    args = parser.parse_args()

    if args.action == "run-server":
        run_server(args.name, args.transport, args.port)
    elif args.action == "async-example":
        asyncio.run(run_async_example())


if __name__ == "__main__":
    main()