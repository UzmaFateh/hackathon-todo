---
id: 6
title: mcp-todo-skill-creation
stage: misc
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: main
user: user
command: /skill:skill-creator-pro
labels: [mcp, skill-creation, python, todo]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .claude/skills/mcp-todo-skill/SKILL.md
 - .claude/skills/mcp-todo-skill/assets/server_template.py
 - .claude/skills/mcp-todo-skill/references/mcp-concepts.md
 - .claude/skills/mcp-todo-skill/references/user-isolation.md
tests:
 - .claude/skills/skill-creator-pro/scripts/quick_validate.py
---

## Prompt

I want to use Skill Creator Pro skill to create an MCP (Model Context Protocol) skill using the official MCP Python SDK.
SDK reference: https://modelcontextprotocol.github.io/python-sdk/
Create an MCP server skill that exposes todo task management tools for an AI agent.
The skill must be stateless and persist all data in a database.
The MCP skill should define the following tools:
add_task(user_id, title,)
list_tasks(user_id, status?)
complete_task(user_id, task_id)
delete_task(user_id, task_id)
update_task(user_id, task_id, title?)
Each tool should:
Follow MCP tool schemas and best practices
Return structured JSON responses
Handle errors gracefully (e.g., task not found)
Generate:
MCP tool specifications
Python MCP server implementation using the official SDK
Clear instructions for running and registering the MCP skill with Claude Code CLI
The output should be production-ready, minimal, and easy to extend.

## Response snapshot

Created the `mcp-todo-skill` successfully.

Components:
1.  `SKILL.md`: Defines the skill, usage triggers, and implementation workflow.
2.  `references/mcp-concepts.md`: Covers FastMCP setup and tool decoration.
3.  `references/user-isolation.md`: Defines patterns for stateless security and mandatory `user_id` args.
4.  `assets/server_template.py`: Complete, production-ready Python MCP server implementing all 5 requested tools with SQLModel/Postgres persistence.

Validation:
- Passed quick_validate.py check.
- Follows all architectural constraints (Stateless, MCP SDK, Pure Functions).

Instructions:
To use this skill for implementing the backend server:
1. `cp .claude/skills/mcp-todo-skill/assets/server_template.py backend/mcp/server.py`
2. Update database imports to match your project.
3. Run with `fastmcp run backend/mcp/server.py`.

## Outcome

- ✅ Impact: Created reusable MCP skill for todo management.
- 🧪 Tests: Validated structure with internal script.
- 📁 Files: SKILL.md, assets/server_template.py, references/*.md
- 🔁 Next prompts: /sp.plan to design the integration or /sp.tasks to track implementation.
- 🧠 Reflection: Successfully leveraged Skill Creator Pro patterns for high-quality output.

## Evaluation notes (flywheel)

- Failure modes observed: Context7 MCP tool lookup failed (library not found); gathered info via WebFetch.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None
