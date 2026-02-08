---
name: openai-agents-gemini
description: |
  [What] Creates an OpenAI Agents SDK setup using Gemini as the backend LLM.
  [When] Use when users want to run OpenAI Agents with Google Gemini models via the OpenAI-compatible API.
allowed-tools: Write, Read
---

# OpenAI Agents SDK (Gemini Backend)

Creates a functional OpenAI Agents SDK skill configured to use Google's Gemini models via the OpenAI-compatible API endpoint.

## What This Skill Does
- Configures `AsyncOpenAI` client to point to `generativelanguage.googleapis.com`.
- Implements `OpenAIChatCompletionsModel` using the custom client.
- Defines functional tools (`@function_tool`) for the agent.
- Provides a runnable script (`agent_gemini.py`) using `Runner.run_sync`.
- Sets up `.env` template for keys.

## What This Skill Does NOT Do
- Use real OpenAI models (GPT-4, etc.) unless reconfigured.
- Handle OAuth for Google Cloud (uses API Key auth).
- Deploy the agent to a server (runs locally).

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing `.env` file location, Python dependency management (poetry/pip). |
| **Conversation** | User's specific API key availability (GEMINI_API_KEY). |
| **Skill References** | `references/gemini-config.md` for client setup details. |
| **User Guidelines** | Preference for sync vs async runner. |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Output Checklist
- [ ] Runnable Python script `agent_gemini.py` created.
- [ ] `.env` file (or template) created with `GEMINI_API_KEY`.
- [ ] `AsyncOpenAI` client uses correct Google base_url.
- [ ] Agent instantiated with `model=llm_model` wrapper.
- [ ] Tools defined and attached to Agent.

## Reference Files
| File | When to Read |
|------|--------------|
| `references/gemini-config.md` | For deeper understanding of the Gemini/OpenAI adapter pattern. |
| `assets/agent_gemini.py` | The complete source code implementation. |

## Usage Instructions
1. **Install Dependencies**:
   ```bash
   pip install openai-agents python-dotenv
   ```
2. **Setup Environment**:
   Create `.env`:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_key
   OPENAI_API_KEY=dummy_val_for_tracing
   ```
3. **Run Agent**:
   ```bash
   python agent_gemini.py
   ```
