---
id: 1
title: "AI Todo Chatbot Constitution"
stage: constitution
date_iso: "2026-01-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution Write a Phase III project constitution for an AI-powered Todo Chatbot..."
labels: ["constitution", "ai", "mcp", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - ".specify/memory/constitution.md"
tests_yaml: |
  - "none"
---

# Prompt

```text
Write a Phase III project constitution for an AI-powered Todo Chatbot that builds on an existing authenticated full-stack Todo application. This constitution must define strict rules, scope, and engineering principles for implementing a natural-language chatbot using OpenAI Agents SDK, OpenAI ChatKit (frontend), and an MCP server (Official MCP SDK) that exposes task operations as stateless tools.

The constitution must enforce the following non-negotiable rules:
- The backend FastAPI server and MCP tools must be completely stateless; all conversation state and task data must persist only in Neon Serverless PostgreSQL.
- The AI agent must never access the database directly and must manage tasks exclusively through MCP tools.
- The chatbot must support all Basic-level task features (add, list, update, complete, delete) via natural language.
- Authentication is already implemented (Better Auth + JWT from Phase II) and must be reused without modification.
- The frontend must integrate OpenAI ChatKit inside an existing Next.js chat route only; no new frontend architecture changes are allowed.
- The system must be scalable, deterministic, and production-oriented.

Code quality and tooling rules:
- Whenever any code is written, updated, or referenced, Claude must use the Context-7 MCP skill to ensure all APIs, SDK usage, and patterns are modern, correct, and up to date.
- Claude must not use deprecated APIs, outdated patterns, or memory-based implementations.
- All behavior must be spec-driven, tool-first, and aligned with MCP architecture principles.

The constitution should clearly define:
- Phase III objectives and non-goals
- AI agent behavior rules
- MCP tool governance rules
- Stateless architecture guarantees
- Security and user isolation requirements
- Evaluation criteria for judging success in Phase III
```

# Response

Constitution created successfully with the following key principles:

## Core Principles
1. Stateless Architecture (NON-NEGOTIABLE) - All state in PostgreSQL only
2. MCP-Only Data Access (NON-NEGOTIABLE) - AI agent never accesses DB directly
3. Natural Language Task Operations - Support all Basic-level features via natural language
4. Authentication Reuse - Reuse existing Better Auth + JWT without modification
5. Frontend Integration Constraints - OpenAI ChatKit only in existing route
6. Scalability and Determinism - Production-oriented requirements
7. MCP Architecture Compliance - Spec-driven, tool-first approach
8. Context-7 MCP Skill Usage (NON-NEGOTIABLE) - For all API/SDK references

## Additional Sections
- AI Agent Behavior Rules
- MCP Tool Governance Rules
- Stateless Architecture Guarantees
- Security and User Isolation Requirements
- Evaluation Criteria for Phase III Success
- Development Workflow
- Governance

The constitution enforces the non-negotiable rules specified in the requirements and provides a framework for implementing the AI-powered Todo Chatbot while maintaining architectural integrity and security.