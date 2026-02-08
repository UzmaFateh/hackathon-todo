# Stateless User Isolation Patterns

## Principle
Every tool invocation is independent. No session state is stored in the MCP server memory.

## Pattern
1. **Explicit `user_id` Argument**:
   - Every tool MUST accept `user_id` as its first argument.
   - The caller (LLM or Agent Driver) is responsible for providing the correct `user_id`.

2. **Database Persistence**:
   - All state resides in PostgreSQL.
   - Tools act as pure transaction handlers: `Tool(args) -> DB Transaction -> Result`.

3. **Validation**:
   - Validate `user_id` format if necessary.
   - Ensure operations explicitly filter by `user_id` in SQL queries (e.g., `WHERE user_id = ?`).

4. **Return Values**:
   - Return clean, minimal JSON-serializable dictionaries.
   - Avoid returning raw ORM objects; convert to dicts or Pydantic models first.

## Example Signature
```python
@mcp.tool()
def add_task(user_id: str, title: str) -> dict:
    """Add a new task for a specific user."""
    # 1. Connect to DB
    # 2. Insert with user_id
    # 3. Return dict(id=..., title=..., status=...)
```
