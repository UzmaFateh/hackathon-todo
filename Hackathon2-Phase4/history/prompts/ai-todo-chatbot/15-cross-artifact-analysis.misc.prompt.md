---
id: 15
title: cross-artifact spec plan tasks analysis
stage: misc
date: 2026-01-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: ahmednoorani
command: /sp.analyze
labels: [analysis, spec, plan, tasks]
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

<command-message>sp.analyze</command-message>
<command-name>/sp.analyze</command-name>## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This command MUST run only after `/sp.tasks` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside `/sp.analyze`.

## Execution Steps

### 1. Initialize Analysis Context

Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).
For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases (if present)

**From plan.md:**

- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**

- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution:**

- Load `.specify/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: Each functional + non-functional requirement with a stable key (derive slug based on imperative phrase; e.g., "User can upload file" → `user-can-upload-file`)
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories (inference by keyword / explicit reference patterns like IDs or key phrases)
- **Constitution rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

### 5. Severity Assignment

### 6. Produce Compact Analysis Report

### 7. Provide Next Actions

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

## Context

$ARGUMENTS

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

## Response snapshot

Executed a read-only cross-artifact analysis across `specs/001-ai-todo-chatbot/spec.md`, `plan.md`, `tasks.md`, and `.specify/memory/constitution.md`. Reported CRITICAL issues (plan.md placeholders, endpoint path mismatch in spec narrative vs contract, repository structure drift vs constitution, missing coverage for clarifying-question behavior and performance NFR), plus coverage mapping and recommended next actions. Noted that the PowerShell prerequisite script could not run due to missing `pwsh`.

## Outcome

- ✅ Impact: Identified blocking inconsistencies/underspecification before implementation.
- 🧪 Tests: none
- 📁 Files: none
- 🔁 Next prompts: Fill/approve plan.md, reconcile endpoint naming, add missing task coverage, then re-run /sp.analyze and proceed to /sp.implement.
- 🧠 Reflection: In this repo, unfilled plan templates and architecture drift are the dominant sources of rework.

## Evaluation notes (flywheel)

- Failure modes observed: `pwsh` not available, so check-prerequisites.ps1 could not be executed as prescribed.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): Ensure PowerShell availability (or a non-pwsh fallback) so analysis workflows can reliably auto-detect FEATURE_DIR and docs.
