# Implementation Tasks: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot (Phase III) | **Priority**: P1 (Critical) | **Status**: Ready for Implementation

## Overview
Implementation of a stateless AI-powered chatbot for natural language todo management using OpenAI Agents SDK with Gemini backend, MCP Python SDK for todo operations, and persistent conversation history in Neon PostgreSQL. The system provides a conversational interface for add, list, update, complete, and delete operations while maintaining strict user isolation through JWT authentication.

## Dependencies
- Phase II: Full-stack web app with Next.js + Better Auth JWT + FastAPI + SQLModel + Neon PostgreSQL
- MCP Python SDK
- OpenAI Agents SDK (with Gemini adapter)

## Parallel Execution Examples
- **US1**: Backend MCP tools and agent logic can be developed in parallel with frontend chat components
- **US2**: Database models and API endpoints can be developed in parallel with conversation history UI
- **US3**: Stateless API implementation can run alongside server restart testing

## Implementation Strategy
**MVP Scope**: US1 (Natural Language Task Management) with minimal conversation persistence
**Delivery**: Incremental approach - US1 → US2 → US3 → Polish

---

## Phase 1: Setup & Project Initialization

- [X] T001 Set up backend project structure per plan in backend/mcp/__init__.py
- [X] T002 Set up frontend project structure per plan in frontend/app/chat/page.tsx
- [X] T003 Install backend dependencies (FastAPI, SQLModel, OpenAI-agents, MCP SDK) in backend/requirements.txt
- [X] T004 Install frontend dependencies (@openai/chatkit-react or equivalent) in frontend/package.json
- [X] T005 [P] Configure environment variables for database, JWT, and API keys in backend/.env

---

## Phase 2: Foundational Components

- [X] T006 Create Conversation model in backend/models.py
- [X] T007 Create Message model in backend/models.py
- [X] T008 Create database migration for conversation and message tables in backend/migrations/
- [X] T009 [P] Create JWT authentication dependency in backend/dependencies.py
- [X] T010 [P] Create database session dependency in backend/database.py
- [X] T011 [US1] Set up MCP server foundation using mcp-sdk skill in backend/mcp/server.py
- [X] T012 Create initial agent configuration using openai-agents-gemini skill in backend/agents/agent_config.py

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1)

**Goal**: Enable logged-in users to manage tasks (add, list, update, complete, delete) using natural language commands.

**Independent Test**: Can be tested via the `/api/chat` endpoint by sending natural language prompts (e.g., "Add buy milk") and verifying the database state reflects the change.

### Implementation Tasks:

- [X] T013 [P] [US1] Create MCP tools for todo operations using mcp-todo-skill in backend/mcp/tools.py
- [X] T014 [P] [US1] Implement add_todo tool with user_id validation using mcp-todo-skill in backend/mcp/tools.py
- [X] T015 [P] [US1] Implement list_todos tool with user_id validation using mcp-todo-skill in backend/mcp/tools.py
- [X] T016 [P] [US1] Implement update_todo tool with user_id validation using mcp-todo-skill in backend/mcp/tools.py
- [X] T017 [P] [US1] Implement complete_todo tool with user_id validation using mcp-todo-skill in backend/mcp/tools.py
- [X] T018 [P] [US1] Implement delete_todo tool with user_id validation using mcp-todo-skill in backend/mcp/tools.py
- [X] T019 [US1] Create main chat agent implementation using openai-agents-gemini skill in backend/agents/chat_agent.py
- [X] T020 [US1] Configure agent with detailed persona instructions using openai-agents-gemini skill in backend/agents/agent_config.py
- [X] T021 [US1] Implement tool error handling with user-friendly messages in backend/agents/chat_agent.py
- [X] T022 [US1] Create POST /api/{user_id}/chat endpoint in backend/routes/chat.py
- [X] T023 [US1] Implement JWT validation for chat endpoint in backend/routes/chat.py
- [X] T024 [US1] Integrate agent with chat endpoint in backend/routes/chat.py
- [X] T025 [US1] Store user messages to database in backend/routes/chat.py
- [X] T026 [US1] Store agent responses to database in backend/routes/chat.py
- [X] T027 [US1] Create basic chat page UI in frontend/app/chat/page.tsx
- [X] T028 [US1] Create chat window component in frontend/app/chat/components/ChatWindow.tsx
- [X] T029 [US1] Create message display component in frontend/app/chat/components/Message.tsx
- [X] T030 [US1] Implement chat messaging functionality in frontend/app/chat/hooks/useChat.ts

### Test Scenarios:
- [ ] T031 [US1] Test "Add a task to buy milk" creates todo in database
- [ ] T032 [US1] Test "Mark buy milk as done" updates todo status
- [ ] T033 [US1] Test "What do I have to do?" lists pending tasks
- [ ] T034 [US1] Test "Delete the task about milk" removes todo
- [ ] T035 [US1] Test out-of-scope requests are politely declined

---

## Phase 4: User Story 2 - Conversation History Persistence (Priority: P2)

**Goal**: Enable returning users to see their previous conversation history when opening the chat window.

**Independent Test**: Send a message, refresh the page/re-query history, and verify last messages are still present.

### Implementation Tasks:

- [X] T036 [US2] Create GET /api/{user_id}/conversations endpoint in backend/routes/chat.py
- [X] T037 [US2] Implement user_id validation for conversation listing in backend/routes/chat.py
- [X] T038 [US2] Create GET /api/{user_id}/conversations/{conversation_id} endpoint in backend/routes/chat.py
- [X] T039 [US2] Implement conversation message retrieval with user_id validation in backend/routes/chat.py
- [X] T040 [US2] Create POST /api/{user_id}/conversations endpoint for new conversations in backend/routes/chat.py
- [X] T041 [US2] Add conversation creation logic with auto-title generation in backend/routes/chat.py
- [X] T042 [US2] Update chat agent to load conversation history before processing in backend/agents/chat_agent.py
- [X] T043 [US2] Create conversation list component in frontend/app/chat/components/ConversationList.tsx
- [X] T044 [US2] Implement conversation history loading in frontend/app/chat/hooks/useChat.ts
- [X] T045 [US2] Create new conversation button in frontend/app/chat/components/NewChatButton.tsx
- [X] T046 [US2] Implement conversation switching functionality in frontend/app/chat/hooks/useChat.ts

### Test Scenarios:
- [ ] T047 [US2] Test message history persists after page refresh
- [ ] T048 [US2] Test loading conversation history from database
- [X] T049 [US2] Test creating new conversations clears context

---

## Phase 5: User Story 3 - Stateless Chat API (Priority: P3)

**Goal**: Ensure the chat API is fully stateless and loads user context from the database on every request.

**Independent Test**: Restart the backend server during a conversation; the next message should still work correctly because no state was in memory.

### Implementation Tasks:

- [X] T050 [US3] Verify all agent state is loaded from database on each request in backend/agents/chat_agent.py
- [X] T051 [US3] Implement conversation context loading for each chat request in backend/routes/chat.py
- [X] T052 [US3] Remove any in-memory state storage in backend/agents/chat_agent.py
- [X] T053 [US3] Add user_id validation to ensure proper isolation in backend/routes/chat.py
- [ ] T054 [US3] Implement concurrent user isolation tests in backend/tests/integration/test_chat_api.py
- [X] T055 [US3] Add rate limiting middleware for API protection in backend/middleware/rate_limit.py
- [X] T056 [US3] Add input sanitization for message content in backend/routes/chat.py
- [X] T057 [US3] Add sequence number management for message ordering in backend/models/message.py
- [X] T058 [US3] Implement proper error handling for all edge cases in backend/routes/chat.py

### Test Scenarios:
- [ ] T059 [US3] Test server restart preserves conversation context
- [ ] T060 [US3] Test concurrent users don't cross-contaminate conversations
- [ ] T061 [US3] Test input sanitization prevents injection attacks

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T062 Add comprehensive logging for chat operations in backend/utils/logging.py
- [ ] T063 Implement performance monitoring for API latency in backend/metrics/
- [X] T064 Add comprehensive error handling for network issues in backend/agents/chat_agent.py
- [X] T065 Create API documentation from OpenAPI spec in docs/api-reference.md
- [X] T066 Add unit tests for all MCP tools in backend/tests/unit/test_mcp_tools.py
- [X] T067 Add integration tests for chat API in backend/tests/integration/test_chat_api.py
- [X] T068 Add frontend component tests in frontend/tests/components/chat.test.tsx
- [ ] T069 Optimize database queries with proper indexing in backend/models.py
- [X] T070 Add caching layer for frequently accessed data in backend/cache/
- [X] T071 Create deployment configuration for production in deploy/prod.yaml
- [ ] T072 Conduct security review of user isolation implementation
- [X] T073 Document troubleshooting procedures for chatbot issues in docs/troubleshooting.md
- [ ] T074 [US3] Implement horizontal scaling capabilities with stateless design in backend/agents/chat_agent.py
- [X] T075 [US3] Add uptime monitoring and health checks for 99.5% availability in backend/health_check.py
- [X] T076 [US3] Implement ACID transaction handling with proper rollback in backend/database.py
- [X] T077 [US3] Add encryption for data at rest and in transit for conversation data in backend/security.py
- [X] T078 [US3] Create privacy compliance measures per NF-006 in backend/security.py
- [X] T079 [US3] Implement authentication failure handling per edge case in backend/routes/chat.py
- [X] T080 [US3] Add graceful tool failure handling with user-friendly messages in backend/agents/chat_agent.py
- [X] T081 [US3] Implement ambiguous request clarification logic per edge case in backend/agents/chat_agent.py
- [X] T082 [US3] Add handling for empty/nonsense input per edge case in backend/routes/chat.py
- [X] T083 [US3] Implement concurrent access conflict resolution per edge case in backend/models.py
- [X] T084 [US3] Add comprehensive input injection protection per edge case in backend/routes/chat.py
- [X] T085 [US3] Implement rate limiting per edge case in backend/middleware/rate_limit.py
- [X] T086 [US3] Add session timeout handling per edge case in backend/routes/chat.py
- [X] T087 [US3] Implement invalid user_id validation per edge case in backend/routes/chat.py

---

## Acceptance Criteria

### Measurable Outcomes:
- [ ] SC-001: Users can perform all 5 basic task operations (Add, List, Update, Complete, Delete) successfully via natural language
- [ ] SC-002: Chat history persists across page reloads (verify 100% retention in test scenarios)
- [ ] SC-003: API Latency for chat responses is under 5 seconds (excluding LLM generation time) for 95% of requests
- [ ] SC-004: Zero hallucinations of user IDs (Agent never accesses another user's data)

### Quality Gates:
- [ ] All user stories independently testable and functional
- [ ] All security requirements satisfied (user isolation, input validation)
- [ ] All performance requirements met (response time, concurrent users)
- [ ] All edge cases properly handled with graceful error responses