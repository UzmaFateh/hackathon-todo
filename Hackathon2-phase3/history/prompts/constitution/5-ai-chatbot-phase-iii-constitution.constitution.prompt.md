---
id: 5
title: ai-chatbot-phase-iii-constitution
stage: constitution
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, phase-iii, ai-chatbot, mcp, openai-agents]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - CLAUDE.md
tests:

---

## Prompt

You are working inside the "hackathon-todo" monorepo project.
We have completed Phase II (full-stack web app with Next.js + Better Auth JWT + FastAPI + SQLModel + Neon PostgreSQL).

Now we are starting **Phase III**: AI-powered conversational chatbot for natural language todo management.

Your task is to **update and significantly improve** your current constitution (the CLAUDE.md file(s) that define how you should behave, think, and code in this project) so that you become much more effective for Phase III work.

Please create an **updated version of the root CLAUDE.md** (and suggest any needed additional CLAUDE.md files like backend/CLAUDE.md or mcp/CLAUDE.md if you think they would help).

Important new context & requirements for Phase III:

... [full user prompt content] ...

## Response snapshot

Updated the Constitution to support Phase III: AI-Powered Todo Chatbot.

Key updates:
1.  **Phase III Definition:** Clearly defined goals for AI chatbot, OpenAI Agents SDK, and MCP Python SDK integration.
2.  **Core Principles:** Added strict rules for Stateless Architecture, MCP-Only Data Access, and Context-7 Skill Priority.
3.  **Architecture:** Enforced Async/Await, Dependency Injection, and User Isolation.
4.  **Documentation Links:** Added official links for OpenAI Agents, MCP, FastMCP, ChatKit, and Better Auth.
5.  **Project Structure:** Updated with new `agents/`, `mcp/`, and `chat/` directories.

Files Updated:
- `CLAUDE.md` (Root)
- `.specify/memory/constitution.md` (Master Constitution)

Templates Verified (No changes required for generic compatibility):
- `.specify/templates/plan-template.md`
- `.specify/templates/spec-template.md`
- `.specify/templates/tasks-template.md`

## Outcome

- ✅ Impact: Constitution updated for Phase III AI Chatbot
- 🧪 Tests: None
- 📁 Files: CLAUDE.md, .specify/memory/constitution.md updated
- 🔁 Next prompts: /sp.plan or feature spec creation
- 🧠 Reflection: Strong foundation set for stateless, agentic workflow.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None
