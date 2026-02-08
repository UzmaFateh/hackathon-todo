---
name: mcp-sdk
description: |
  This skill provides guidance for implementing Model Context Protocol (MCP) Python SDK features, including servers, clients, tools, resources, and prompts.
  Use when users ask to implement MCP-compliant services for communication between LLM applications and external services.
---

# Model Context Protocol (MCP) Python SDK Implementation Guide

## Overview

The Model Context Protocol (MCP) Python SDK implements the MCP specification, enabling standardized communication between LLM applications (like Claude Code) and external services. It provides tools for building both MCP servers and clients with multiple transport options.

## Core Features

### Server Creation
- Build MCP servers exposing resources, tools, and prompts
- Use FastMCP for simplified server development
- Support for stateful and stateless operation

### Client Development
- Connect to any MCP server
- Support for authentication (OAuth)
- Multiple transport protocols

### Transport Support
- stdio: Traditional stdin/stdout communication
- SSE: Server-Sent Events for streaming
- Streamable HTTP: HTTP-based transport with bidirectional communication

### Protocol Compliance
- Full MCP specification implementation
- Built-in connection management
- Message routing and validation

## Installation

```bash
pip install "mcp[cli]"
```

Or with uv:
```bash
uv add "mcp[cli]"
```

## Core Concepts

### Tools
Functional operations exposed by MCP servers (similar to POST endpoints)
- Perform actions and return results
- Support both sync and async functions
- Can maintain state across calls

### Resources
Data access endpoints (similar to GET endpoints)
- Provide access to data sources
- Support for various data types
- Streaming capabilities

### Prompts
Reusable LLM interaction templates
- Predefined message sequences
- Parameterized prompt templates
- Structured conversation flows

## Implementation Patterns

### FastMCP Server Example
```python
from mcp.server.fastmcp import FastMCP

# Create a simple server
mcp = FastMCP("Demo Server", json_response=True)

# Define a tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

# Define a resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Define a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }
    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

# Run the server
if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=3000)
```

### Async Tool Example
```python
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("HTTP Tools Server")

@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/current?city={city}")
        return response.text
```

### Image Tool Example
```python
from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage

mcp = FastMCP("Image Processing Server")

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")
```

### Prompt with Structured Messages
```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("Code Review Server")

@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:

{code}"

@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]
```

### Server with Dependencies and Lifespan Management
```python
from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

@dataclass
class AppContext:
    db: object  # Your database connection

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Initialize resources on startup, cleanup on shutdown"""
    db = await connect_to_database()
    try:
        yield AppContext(db=db)
    finally:
        await db.disconnect()

mcp = FastMCP("Database Server", lifespan=app_lifespan)
```

### Stateful vs Stateless Servers
```python
from mcp.server.fastmcp import FastMCP

# Stateful server (maintains session state)
stateful_mcp = FastMCP("StatefulServer")

# Stateless server (no session persistence)
stateless_mcp = FastMCP("StatelessServer", stateless_http=True)

# Stateless server with JSON response format
json_mcp = FastMCP("JSONServer", stateless_http=True, json_response=True)
```

## Running Servers

### Streamable HTTP Transport
```bash
uv run mcp-simple-streamablehttp --port 3000
uv run mcp-simple-streamablehttp --log-level DEBUG
uv run mcp-simple-streamablehttp --json-response
```

### Configuration File
```json
{
  "mcpServers": {
    "my_server": {
      "command": "uvx",
      "args": ["my-mcp-server", "--port", "3001"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Client Example
```python
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken

class CustomTokenStorage(TokenStorage):
    """Simple in-memory token storage implementation."""

    async def get_tokens(self) -> OAuthToken | None:
        pass

    async def set_tokens(self, tokens: OAuthToken) -> None:
        pass

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        pass

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        pass

async def main():
    # Set up OAuth authentication
    oauth_auth = OAuthClientProvider(
        server_url="https://api.example.com",
        client_metadata=OAuthClientMetadata(
            client_name="My Client",
            redirect_uris=["http://localhost:3000/callback"],
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
        ),
        storage=CustomTokenStorage(),
        redirect_handler=lambda url: print(f"Visit: {url}"),
        callback_handler=lambda: ("auth_code", None),
    )

    # Use with streamable HTTP client
    async with streamablehttp_client(
        "https://api.example.com/mcp", auth=oauth_auth
    ) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Authenticated session ready
```

## Best Practices

1. **Type Hints**: Use Python type hints for automatic parameter validation
2. **Async Operations**: Use async functions for I/O-bound operations
3. **Error Handling**: Implement proper error handling in tools and resources
4. **Authentication**: Use OAuth for protected endpoints when needed
5. **State Management**: Choose stateful vs stateless based on your needs
6. **Transport Selection**: Select the appropriate transport for your use case
7. **Resource Identification**: Use proper URI schemes for resources

## Security Considerations

- Implement proper authentication for sensitive operations
- Validate all inputs to tools and resources
- Use HTTPS for network communication
- Secure token storage for OAuth clients
- Implement rate limiting for high-volume operations
- Sanitize outputs before sending to clients

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing Python application structure, dependency management, and async patterns |
| **Conversation** | User's specific MCP requirements, transport needs, and security requirements |
| **Skill References** | API patterns from `references/` (servers/clients/tools management) |
| **User Guidelines** | Project-specific conventions, deployment patterns, and integration needs |

Ensure all required context is gathered before implementing.