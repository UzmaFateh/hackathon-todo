<!-- Sync Impact Report:
     Version change: 1.0.0 → 1.1.0
     Modified principles: Source of Truth (Added specific skill mandates), Architecture & Patterns (Refined for skill usage)
     Added sections: Skill Usage Mandates
     Removed sections: None
     Templates requiring updates: None (Generic patterns still valid)
     Follow-up TODOs: None
-->

# Todo App - Hackathon (Constitution - Phase III Update 2026-01)

## Current Project Phase & Goals

We have completed Phase II (full-stack web app with Next.js + Better Auth JWT + FastAPI + SQLModel + Neon PostgreSQL).

Now we are starting **Phase III**: AI-powered conversational chatbot for natural language todo management.

**Core Goals:**
1.  **Conversational Interface:** Natural language todo management (add, list, update, complete, delete).
2.  **OpenAI Agents SDK:** Driver for agent logic, state management, and tool calling.
3.  **MCP Python SDK:** Tools exposed via official Model Context Protocol.
4.  **Stateless Architecture:** No in-memory state; persistent conversation history in Postgres/Neon.
5.  **User Isolation:** Strict JWT validation + user_id path parameter checks for every operation.

## Core Principles & Rules of Behavior

### 1. Source of Truth & Skill Mandates (NON-NEGOTIABLE)
- **Single Source of Truth:** The spec folder (`/specs`) is the authority. Code must match specs.
- **Spec-Driven Development:** No implementation without a corresponding spec update.
- **Context-7 Efficiency:** ALWAYS use the `context7-efficient` skill for library research. Never guess APIs.
- **Specialized Skill Usage (MANDATORY):**
  - **MCP Implementation:** MUST use the `mcp-sdk` skill for all MCP server/tool architectural patterns.
  - **Todo Logic:** MUST use the `mcp-todo-skill` for implementing todo-specific MCP tools and server logic.
  - **Agent Backend:** MUST use the `openai-agents-gemini` skill for configuring the Agent loop with Gemini models (OpenAI-compatible adapter).
  - **Documentation:** MUST use `context7-efficient` to fetch docs before writing any code using external libraries.

### 2. Architecture & Patterns (Phase III)
- **Async First:** Prefer `async/await` in all FastAPI endpoints and dependencies.
- **Dependency Injection:** Use FastAPI `Depends()` for `current_user` (JWT) and `Session`.
- **Stateless Agent:**
    - Never store conversation state in server memory.
    - Always load history from DB (tables: `conversations`, `messages`) on each turn.
    - Expose a stateless `POST /api/{user_id}/chat` endpoint.
- **MCP Tools:**
    - Must be **simple, pure, synchronous functions** returning clean JSON-serializable dictionaries.
    - Follow **official MCP SDK** patterns (see documentation links below).
- **OpenAI Agents SDK:**
    - Use the latest styles (Runner, Agent class, tool calling).
    - Provide precise instructions: when to use tools, how to format responses, when to ask clarifying questions.

### 3. Security & Validation
- **User Isolation:** Every DB query must filter by `user_id`.
- **Auth Reuse:** Reuse Phase II Better Auth JWT plugin; do not invent new auth schemes.
- **Input Validation:** Use Pydantic models for all API inputs/outputs.
- **Zero Hallucination:** If a tool fails or data is missing, fail gracefully or ask the user—never invent IDs or data.

## Official Documentation Links (Use Context-7 to fetch these)

- **OpenAI Agents SDK:** `https://github.com/openai/openai-agents-python`
- **Model Context Protocol (MCP) Python SDK:** `https://github.com/modelcontextprotocol/mcp-python-sdk`
- **FastMCP:** `https://github.com/modelcontextprotocol/fastmcp`
- **OpenAI ChatKit:** `https://platform.openai.com/docs/chatkit`
- **Better Auth JWT:** `https://better-auth.com/docs/plugins/jwt`

## Project Structure (Phase III)

```text
/
├── backend/
│   ├── main.py
│   ├── api/routes/chat.py      # NEW: Chat endpoint
│   ├── agents/                 # NEW: Agent logic (OpenAI SDK)
│   ├── mcp/                    # NEW: MCP Tools implementation
│   │   └── tools.py
│   └── models/                 # Existing + new (Conversation, Message)
├── frontend/
│   ├── app/chat/               # NEW: Chat page (ChatKit)
│   └── components/ui/          # Shared UI
└── specs/
    ├── features/               # Feature specs
    ├── api/                    # API contracts
    └── database/               # Schema specs
```

## Governance

This constitution supersedes all other development practices for Phase III. All code changes must verify compliance with these principles. Complexity must be justified with clear benefits. Use this constitution for runtime development guidance and decision-making. Any changes to these principles require formal amendment process with documentation, approval, and migration planning.

**Version**: 1.1.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-10
