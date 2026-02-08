---
id: 8
title: constitution-skill-usage-mandate
stage: constitution
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, skill-mandate, mcp, openai-agents]
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

update the constituion in which i want to use the claude skill which i just created named mcp-sdk, mcp-todo-skill, openai-agents-gemini, context7-efficient that it should use this skills to do this technology related tasks and its very important to use tbhis skill

## Response snapshot

Updated the Constitution to mandate the use of specific Claude skills for Phase III technology tasks.

Key updates:
1.  **Skill Mandates Section:** Added "Specialized Skill Usage (MANDATORY)" under Core Principles.
2.  **Specific Mandates:**
    *   **MCP Implementation:** Must use `mcp-sdk` skill.
    *   **Todo Logic:** Must use `mcp-todo-skill`.
    *   **Agent Backend:** Must use `openai-agents-gemini` skill.
    *   **Documentation:** Must use `context7-efficient` skill.
3.  **Governance Bump:** Version updated to 1.1.0.

Files Updated:
- `CLAUDE.md` (Root)
- `.specify/memory/constitution.md` (Master Constitution)

## Outcome

- ✅ Impact: Constitution enforced usage of specific high-quality skills.
- 🧪 Tests: None
- 📁 Files: CLAUDE.md, .specify/memory/constitution.md updated
- 🔁 Next prompts: /sp.plan to design the chat system using these mandated skills.
- 🧠 Reflection: Explicit content mandates ensure consistent quality by forcing the agent to use validated patterns from skills.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None
