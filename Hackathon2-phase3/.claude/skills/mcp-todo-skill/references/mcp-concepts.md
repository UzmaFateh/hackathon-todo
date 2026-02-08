# Core MCP Concepts (FastMCP)

## Server Initialization
- `FastMCP` class manages the lifecycle and connections.
- Name parameter in `FastMCP(name="...")` identifies the server.
- Default transport is stdio (`mcp.run()`).

## Tool Definition
- Use `@mcp.tool()` decorator.
- Use type hints (Pydantic models, primitives) for automatic schema generation.
- Tool description comes from the docstring.
- Tools can be sync (`def`) or async (`async def`).

## Context & User Identification
- Tools are stateless but can receive context via `Context` object.
- **Critical Requirement**: Our project requires passing `user_id` explicitly as an argument to every tool for stateless user isolation.
- **Auth**: Authentication happens upstream (FastAPI); tools assume authenticated context if invoked.

## Error Handling
- Exceptions raised in tools are converted to MCP protocol errors.
- Use standard Python exceptions (ValueError, etc.) for logical errors.
- Graceful failure: return structured error responses if partial success is possible, or raise exceptions for blocking failures.

## Resources vs Tools
- **Tools**: Executable actions (add_task, delete_task). Side-effects allowed.
- **Resources**: Read-only data access (file contents, system status). Side-effects discouraged.
- For this skill, we primarily use **Tools** for CRUD operations.

## Database Integration
- Tools should not hold db connections.
- Use dependency injection or context managers for DB sessions per request.
- Ensure connections are closed after tool execution.
