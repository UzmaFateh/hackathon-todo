# Model Context Protocol (MCP) Python SDK Skill

This skill provides guidance and tools for implementing Model Context Protocol (MCP) Python SDK features, including servers, clients, tools, resources, and prompts.

## Components

- `SKILL.md`: Main skill definition with API documentation and implementation guidance
- `references/api-reference.md`: Detailed API reference for MCP SDK
- `scripts/mcp-sdk-helper.py`: Python helper script for common operations

## Installation

```bash
pip install "mcp[cli]"
```

## Usage

The skill provides guidance for:

1. Creating and configuring MCP servers using FastMCP
2. Implementing tools, resources, and prompts
3. Setting up clients with authentication
4. Using different transport protocols (stdio, SSE, Streamable HTTP)
5. Following best practices for MCP development

## Helper Script Commands

```bash
# Run a demo server with stdio transport
python scripts/mcp-sdk-helper.py --action run-server --name "My Server" --transport stdio

# Run a server with streamable HTTP transport
python scripts/mcp-sdk-helper.py --action run-server --name "HTTP Server" --transport streamable-http --port 3001
```

## Key Features

- **Server Creation**: Build MCP servers exposing resources, tools, and prompts
- **Client Development**: Connect to any MCP server
- **Transport Support**: stdio, SSE, and Streamable HTTP
- **Protocol Compliance**: Full MCP specification implementation
- **Authentication**: OAuth support for secure connections