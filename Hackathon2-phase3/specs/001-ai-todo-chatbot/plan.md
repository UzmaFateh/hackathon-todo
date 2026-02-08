# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `001-ai-todo-chatbot` | **Date**: 2026-01-12 | **Spec**: [specs/001-ai-todo-chatbot/spec.md](/specs/001-ai-todo-chatbot/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a stateless AI-powered chatbot for natural language todo management using OpenAI Agents SDK with Gemini backend, MCP Python SDK for todo operations, and persistent conversation history in Neon PostgreSQL. The system provides a conversational interface for add, list, update, complete, and delete operations while maintaining strict user isolation through JWT authentication.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11, TypeScript/JavaScript for frontend
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, MCP Python SDK, Better Auth, SQLModel, Neon PostgreSQL
**Storage**: Neon PostgreSQL with SQLModel ORM
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: web (determines source structure)
**Performance Goals**: API Latency under 3 seconds for 95% of requests, support 100 concurrent users
**Constraints**: <200ms p95 for DB operations, stateless agent design, strict user isolation by user_id
**Scale/Scope**: 10k users, multiple concurrent conversations per user, secure JWT authentication

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Source of Truth Compliance**: ✅ Spec exists at `/specs/001-ai-todo-chatbot/spec.md` with complete requirements
2. **Skill Mandates Compliance**: ✅ Will use `mcp-sdk` for MCP tools, `mcp-todo-skill` for todo logic, `openai-agents-gemini` for agent, `context7-efficient` for research
3. **Architecture Compliance**: ✅ Stateless agent design, async/await patterns, dependency injection with FastAPI Depends()
4. **Security Compliance**: ✅ JWT authentication reuse, user_id filtering, input validation with Pydantic models
5. **MCP Compliance**: ✅ Tools will be pure synchronous functions returning JSON-serializable dictionaries
6. **OpenAI Agents Compliance**: ✅ Using latest SDK patterns with precise instructions

### Post-Design Re-Evaluation

After completing Phase 1 design, all constitution requirements remain satisfied:
- ✅ Data models properly implement user isolation with user_id foreign keys
- ✅ API contracts enforce JWT authentication and user validation
- ✅ MCP tools designed as pure synchronous functions as required
- ✅ Agent implementation follows stateless architecture pattern
- ✅ All security requirements maintained in implementation design

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-todo-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py
├── api/routes/chat.py      # NEW: Chat endpoint
├── agents/                 # NEW: Agent logic (OpenAI SDK)
│   ├── __init__.py
│   ├── chat_agent.py       # Main agent implementation
│   └── agent_config.py     # Agent configuration and instructions
├── mcp/                    # NEW: MCP Tools implementation
│   ├── __init__.py
│   ├── server.py           # MCP server setup
│   └── tools.py            # Todo-specific MCP tools
├── models/                 # Existing + new (Conversation, Message)
│   ├── __init__.py
│   ├── conversation.py     # Conversation model
│   ├── message.py          # Message model
│   └── base.py             # Base model configuration
├── dependencies.py         # JWT auth dependency
└── database.py             # Database session management

frontend/
├── app/chat/               # NEW: Chat page (ChatKit)
│   ├── page.tsx            # Chat interface page
│   ├── components/         # Chat components
│   │   ├── ChatWindow.tsx  # Main chat window
│   │   ├── Message.tsx     # Individual message component
│   │   └── NewChatButton.tsx # New chat session button
│   └── hooks/              # Chat-specific hooks
│       └── useChat.ts      # Chat state management
├── components/ui/          # Shared UI
└── lib/                    # Shared utilities
    └── api.ts              # API client utilities

specs/
├── 001-ai-todo-chatbot/    # Current feature specs
│   ├── spec.md
│   ├── plan.md             # This file
│   ├── research.md
│   ├── data-model.md
│   ├── quickstart.md
│   └── contracts/
└── api/                    # API contracts
    └── chat-openapi.yaml   # Chat API contract
```

**Structure Decision**: Web application with separate backend and frontend components following the existing project architecture. Backend provides stateless chat API with MCP tools, frontend implements ChatKit-based interface.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |