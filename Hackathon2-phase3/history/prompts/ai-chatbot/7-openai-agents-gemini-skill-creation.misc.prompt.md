---
id: 7
title: openai-agents-gemini-skill-creation
stage: misc
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: main
user: user
command: /skill:skill-creator-pro
labels: [openai-agents, gemini, skill-creation, python]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .claude/skills/openai-agents-gemini/SKILL.md
 - .claude/skills/openai-agents-gemini/assets/agent_gemini.py
 - .claude/skills/openai-agents-gemini/references/gemini-config.md
tests:
 - .claude/skills/skill-creator-pro/scripts/quick_validate.py
---

## Prompt

I want to use Skill Creator Pro skill to create an OpenAI Agents SDK–based skill using the official OpenAI Agents Python SDK...
[Requirements: Gemini backend, AsyncOpenAI custom client, specific code structure preserved]

## Response snapshot

Created the `openai-agents-gemini` skill successfully.

Components:
1. `SKILL.md`: Documented usage and integration steps.
2. `references/gemini-config.md`: Explains the adapter pattern for Gemini > OpenAI API.
3. `assets/agent_gemini.py`: Full Python script implementing the user's specific logic (AsyncOpenAI client + OpenAIChatCompletionsModel + @function_tool).

Validation:
- Passed quick_validate.py check.
- Validated structure matches OpenAI Agents SDK patterns.

Instructions:
1. `cp .claude/skills/openai-agents-gemini/assets/agent_gemini.py backend/agents/gemini_agent.py`
2. Install dependencies: `pip install openai-agents python-dotenv`
3. Configure .env with `GEMINI_API_KEY`.

## Outcome

- ✅ Impact: Created reusable skill for running OpenAI Agents with Gemini.
- 🧪 Tests: Validated structure.
- 📁 Files: SKILL.md, agent_gemini.py created.
- 🔁 Next prompts: /sp.plan to design the chat system using this agent foundation.
- 🧠 Reflection: Successfully adapted OpenAI SDK to support non-OpenAI models via custom client injection.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): None
