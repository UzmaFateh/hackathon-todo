---
id: 14
title: sp.implement blocked by spec gates
stage: implement
date: 2026-01-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: ahmednoorani
command: /sp.implement
labels: [implement, gatekeeping, checklists]
links:
  spec: specs/001-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - none
tests:
 - none
---

## Prompt

<command-message>sp.implement</command-message>
<command-name>/sp.implement</command-name>## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - Calculate overall status:
     - **PASS**: All checklists have 0 incomplete items
     - **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     - Display the table with incomplete item counts
     - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     - Wait for user response before continuing
     - If user says "no" or "wait" or "stop", halt execution
     - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

4. **Project Setup Verification**:
   - **REQUIRED**: Create/verify ignore files based on actual project setup

5. Parse tasks.md structure and extract execution flow.

6. Execute implementation following the task plan (phase-by-phase), marking tasks off in tasks.md.

9. Completion validation.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent-native tools when possible.

## Response snapshot

Attempted to start /sp.implement but could not run the PowerShell prerequisites script because `pwsh` is not available in the current environment. Checked the feature checklist and found incomplete items. Also enforced the spec-authority gate which reported NO-GO because `specs/001-ai-todo-chatbot/plan.md` is still an unfilled template (placeholders like `[FEATURE]`, `NEEDS CLARIFICATION`) and `spec.md` is still marked `Status: Draft`. Implementation was stopped pending checklist confirmation and Phase II spec completion.

## Outcome

- ✅ Impact: Prevented implementation before Phase II specs/checklists are complete.
- 🧪 Tests: none
- 📁 Files: none
- 🔁 Next prompts: Fill/approve `specs/001-ai-todo-chatbot/plan.md` (and resolve inconsistencies), then re-run `/sp.implement`.
- 🧠 Reflection: Enforcing spec completeness up-front avoids code/spec drift and prevents automation scripts from propagating placeholder values.

## Evaluation notes (flywheel)

- Failure modes observed: `pwsh` missing so prerequisite script couldn’t run; `plan.md` still placeholders; checklist contains unchecked items.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): Install/enable PowerShell (`pwsh`) for prerequisite scripts and ensure `/sp.plan` fully populates `plan.md` before `/sp.implement`.
