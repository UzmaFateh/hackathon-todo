# Todo App - Hackathon Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-12

## Active Technologies

**Backend**: Python 3.11, FastAPI, SQLModel, Neon PostgreSQL
**Frontend**: TypeScript/JavaScript, Next.js, React
**Authentication**: Better Auth with JWT
**AI Integration**: OpenAI Agents SDK, MCP Python SDK
**LLM**: Google Gemini (via OpenAI-compatible adapter)
**Database**: Neon PostgreSQL with SQLModel ORM
**Testing**: pytest, Jest

## Project Structure

```text
/
├── backend/
│   ├── main.py
│   ├── api/routes/chat.py      # NEW: Chat endpoint
│   ├── agents/                 # NEW: Agent logic (OpenAI SDK)
│   │   ├── __init__.py
│   │   ├── chat_agent.py       # Main agent implementation
│   │   └── agent_config.py     # Agent configuration and instructions
│   ├── mcp/                    # NEW: MCP Tools implementation
│   │   ├── __init__.py
│   │   ├── server.py           # MCP server setup
│   │   └── tools.py            # Todo-specific MCP tools
│   ├── models/                 # Existing + new (Conversation, Message)
│   │   ├── __init__.py
│   │   ├── conversation.py     # Conversation model
│   │   ├── message.py          # Message model
│   │   └── base.py             # Base model configuration
│   ├── dependencies.py         # JWT auth dependency
│   └── database.py             # Database session management
├── frontend/
│   ├── app/chat/               # NEW: Chat page (ChatKit)
│   │   ├── page.tsx            # Chat interface page
│   │   ├── components/         # Chat components
│   │   │   ├── ChatWindow.tsx  # Main chat window
│   │   │   ├── Message.tsx     # Individual message component
│   │   │   └── NewChatButton.tsx # New chat session button
│   │   └── hooks/              # Chat-specific hooks
│   │       └── useChat.ts      # Chat state management
│   ├── components/ui/          # Shared UI
│   └── lib/                    # Shared utilities
│       └── api.ts              # API client utilities
└── specs/
    └── 001-ai-todo-chatbot/    # Current feature specs
        ├── spec.md
        ├── plan.md             # This file
        ├── research.md
        ├── data-model.md
        ├── quickstart.md
        └── contracts/
```

## Commands

**Backend Development**:
```bash
cd backend
pip install fastapi uvicorn sqlmodel python-multipart better-exceptions openai python-mcp
uvicorn main:app --reload
```

**Frontend Development**:
```bash
cd frontend
npm install @openai/chatkit-react  # Or equivalent for the chat UI
npm run dev
```

**Database Migrations**:
```bash
# Using alembic or similar migration tool
alembic revision --autogenerate -m "Add conversation and message models"
alembic upgrade head
```

**Testing**:
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Code Style

**Python**:
- Use async/await for all FastAPI endpoints and dependencies
- Use FastAPI Depends() for current_user (JWT) and Session injection
- Follow PEP 8 guidelines
- Use type hints everywhere
- Implement proper error handling with Pydantic models

**TypeScript/JavaScript**:
- Use functional components with hooks in React
- Implement proper TypeScript typing
- Follow Next.js best practices
- Use proper error boundaries

## Recent Changes

**AI-Powered Todo Chatbot (Feature 001)**: Added stateless chat API with OpenAI Agents SDK integration, MCP Python SDK for todo operations, conversation and message models for persistent history, and frontend chat interface with ChatKit.

**Foundation Setup (Feature 006)**: Initial project setup with Next.js frontend, FastAPI backend, Better Auth authentication, SQLModel ORM, and Neon PostgreSQL database.

**Task Organization (Feature 007)**: Implemented todo management system with CRUD operations, user isolation, and responsive UI components.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->