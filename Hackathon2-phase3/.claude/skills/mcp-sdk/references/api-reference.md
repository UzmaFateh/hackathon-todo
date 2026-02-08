# Model Context Protocol (MCP) Python SDK API Reference

## Core Classes

### FastMCP
The main class for creating MCP servers with simplified configuration.

**Constructor Parameters:**
- `name` (str): Name of the server
- `stateless_http` (bool, optional): Whether to run in stateless mode (default: False)
- `json_response` (bool, optional): Whether to use JSON response format (default: False)
- `dependencies` (list, optional): List of dependencies for the server
- `lifespan` (callable, optional): Lifespan context manager for resource management

**Usage:**
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Server", json_response=True)
```

### Decorators

#### @mcp.tool()
Decorator to register a function as an MCP tool.

**Usage:**
```python
@mcp.tool()
def my_tool(param1: str, param2: int) -> str:
    """Description of what this tool does."""
    return "result"
```

#### @mcp.resource(uri_template)
Decorator to register a function as an MCP resource.

**Parameters:**
- `uri_template` (str): URI template for the resource

**Usage:**
```python
@mcp.resource("my-resource://{id}")
def get_resource(id: str) -> str:
    """Get a resource by ID."""
    return f"Resource {id}"
```

#### @mcp.prompt()
Decorator to register a function as an MCP prompt.

**Usage:**
```python
@mcp.prompt()
def my_prompt(name: str) -> str:
    """Generate a prompt."""
    return f"Hello, {name}!"
```

## Data Types

### Image
Data type for image resources.

**Constructor Parameters:**
- `data` (bytes): Image data
- `format` (str): Image format (e.g., "png", "jpeg")

**Usage:**
```python
from mcp.server.fastmcp import Image

return Image(data=image_bytes, format="png")
```

### Message Types
Structured message types for prompts.

- `base.UserMessage`: User message in a conversation
- `base.AssistantMessage`: Assistant message in a conversation
- `base.SystemMessage`: System message in a conversation

**Usage:**
```python
from mcp.server.fastmcp.prompts import base

return [
    base.UserMessage("User message content"),
    base.AssistantMessage("Assistant message content"),
]
```

## Transport Options

### Running with Different Transports
```python
# Streamable HTTP transport
mcp.run(transport="streamable-http", port=3000)

# Stdio transport
mcp.run(transport="stdio")

# SSE transport
mcp.run(transport="sse")
```

## Client Classes

### OAuthClientProvider
Handles OAuth authentication for MCP clients.

**Constructor Parameters:**
- `server_url` (str): URL of the MCP server
- `client_metadata` (OAuthClientMetadata): OAuth client metadata
- `storage` (TokenStorage): Token storage implementation
- `redirect_handler` (callable): Handler for redirect URLs
- `callback_handler` (callable): Handler for callback processing

### ClientSession
Manages communication session with an MCP server.

**Usage:**
```python
async with ClientSession(read, write) as session:
    await session.initialize()
    # Session is ready for communication
```

### TokenStorage
Abstract base class for token storage implementations.

**Methods to Implement:**
- `get_tokens()`: Get stored tokens
- `set_tokens(tokens)`: Store tokens
- `get_client_info()`: Get stored client information
- `set_client_info(client_info)`: Store client information

## Configuration

### Environment Variables
Common environment variables for MCP servers:
- `MCP_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `MCP_PORT`: Port number for HTTP transports
- `MCP_TRANSPORT`: Default transport type

### Configuration File Format
```json
{
  "mcpServers": {
    "server_name": {
      "command": "uvx",
      "args": ["mcp-server-name", "--additional-args"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Authentication

### OAuth Client Metadata
Configuration for OAuth clients:
- `client_name` (str): Name of the OAuth client
- `redirect_uris` (list): List of allowed redirect URIs
- `grant_types` (list): Supported grant types
- `response_types` (list): Supported response types

### OAuth Token
Structure for OAuth tokens:
- `access_token` (str): Access token
- `refresh_token` (str): Refresh token (optional)
- `expires_in` (int): Token expiration in seconds
- `token_type` (str): Token type (usually "Bearer")

## Command Line Usage

### Running MCP Servers
```bash
# Basic server with streamable HTTP
uv run mcp-simple-streamablehttp --port 3000

# With debug logging
uv run mcp-simple-streamablehttp --log-level DEBUG

# With JSON response format
uv run mcp-simple-streamablehttp --json-response
```

### Installing MCP Server
```bash
# Install with CLI support
pip install "mcp[cli]"

# Or with uv
uv add "mcp[cli]"
```

## Server Types

### Stateful vs Stateless
- **Stateful**: Maintains session state across requests (default)
- **Stateless**: No session persistence between requests
  - Use `stateless_http=True` for stateless operation
  - More suitable for serverless deployments

### JSON Response Format
- Use `json_response=True` for simplified JSON responses
- Useful for clients that expect consistent JSON format
- Works with `stateless_http=True` for simpler client integration

## Error Handling

### Common Error Types
- `McpError`: Base error class for MCP operations
- `CallToolResult`: Result wrapper that can contain errors

### Tool Result Structure
Tools should return structured results:
- Success: `CallToolResult.success(content)`
- Error: `CallToolResult.error(message)`

## Development Workflow

### Creating a New MCP Server
1. Install the SDK: `pip install "mcp[cli]"`
2. Create a new Python file for your server
3. Initialize FastMCP: `mcp = FastMCP("Server Name")`
4. Add tools/resources/prompts with decorators
5. Run with `mcp.run(transport="...")`

### Testing MCP Servers
- Use Claude Code or other MCP-compatible clients
- Test with different transport methods
- Validate tool parameters and return types
- Test error handling scenarios