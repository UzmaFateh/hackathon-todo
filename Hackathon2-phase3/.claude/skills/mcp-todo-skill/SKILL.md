---
name: mcp-todo-skill
description: |
  [What] Creates a stateless MCP server for todo management.
  [When] Use when users ask to manage todos via AI, set up an MCP server for tasks, or implement the 'todo' toolset for conversational agents.
allowed-tools: Write, Read
---

# MCP Todo Skill

Creates a production-ready, stateless Model Context Protocol (MCP) server for managing todo tasks.

## What This Skill Does
- Generates a fully functional Python MCP server using `FastMCP`.
- Implements 5 core tools: `add`, `list`, `complete`, `delete`, `update`.
- Enforces strict user isolation via `user_id` arguments.
- Persists data to PostgreSQL.
- Provides instructions for running and registering the server.

## What This Skill Does NOT Do
- Handle user authentication (assumes `user_id` is provided by trusted caller).
- Create the database schema (assumes existing or external setup).
- Deploy the server (provides local execution instructions only).

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | DB connection details (`DATABASE_URL`), existing SQLModel definitions. |
| **Conversation** | Specific user needs (custom fields, extra status types?). |
| **Skill References** | `references/mcp-concepts.md` (server setup), `references/user-isolation.md` (security). |
| **User Guidelines** | Project naming conventions, architectural constraints (statelessness). |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Implementation Workflow

1. **Verify Prerequisites**:
   - Python 3.10+
   - `mcp` SDK installed
   - `sqlmodel` and `psycopg2-binary` (or asyncpg) installed

2. **Generate Server Code**:
   - Use `assets/server_template.py` as the base.
   - Adjust `DATABASE_URL` and `TodoTask` model definition to match `backend/models.py` if available.

3. **Register Extension**:
   - Create a `claude_mcp_config.json` entry or update `.claude/mcp-config.json`.
   - Command: `uvicorn mcp_server:mcp.app` or `python mcp_server.py`.

4. **Verify Tools**:
   - Ensure all 5 tools are exposed.
   - Check error handling (try accessing non-existent task).

## Output Checklist
- [ ] Server instantiates `FastMCP("Todo Manager")`.
- [ ] 5 tools implemented: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`.
- [ ] All tools accept `user_id` as first argument.
- [ ] No global state or in-memory storage used.
- [ ] Returns strictly typed dictionaries/JSON.

## Reference Files
| File | When to Read |
|------|--------------|
| `references/mcp-concepts.md` | For FastMCP specifics & error handling patterns. |
| `references/user-isolation.md` | For security & stateless design rules. |
| `assets/server_template.py` | Source code for the MCP server implementation. |
