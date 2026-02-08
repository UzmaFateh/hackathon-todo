# CLI API Contract: Todo In-Memory Python Console Application

## Overview
This document defines the command-line interface contracts for the todo application. All commands follow the Typer framework conventions and use standard input/output streams.

## Command Structure
```
todo [COMMAND] [OPTIONS]
```

## Commands

### 1. Add Task
**Command**: `todo add`

**Parameters**:
- `--title` (required, str): Task title (min 1 char, max 255 chars)
- `--description` (optional, str): Task description (max 1000 chars)
- `--priority` (optional, enum): Priority level [high, medium, low] (default: medium)
- `--tags` (optional, list): List of tags (max 50 chars each)

**Response**:
- Success: "Task created successfully with ID: {task_id}"
- Error: Error message to stderr

**Example**:
```bash
todo add --title "Buy groceries" --priority high --tags shopping urgent
```

### 2. List Tasks
**Command**: `todo list`

**Parameters**:
- `--status` (optional, enum): Filter by completion status [completed, incomplete, all] (default: all)
- `--priority` (optional, enum): Filter by priority [high, medium, low]
- `--search` (optional, str): Search keyword to match in title/description
- `--tags` (optional, list): Filter by specific tags

**Response**:
- Success: Formatted table of tasks with ID, title, status, priority, tags, and creation date
- Error: Error message to stderr

**Example**:
```bash
todo list --status incomplete --priority high
```

### 3. Update Task
**Command**: `todo update`

**Parameters**:
- `--id` (required, str): Task ID to update
- `--title` (optional, str): New title
- `--description` (optional, str): New description
- `--priority` (optional, enum): New priority [high, medium, low]
- `--tags` (optional, list): New list of tags

**Response**:
- Success: "Task updated successfully"
- Error: Error message to stderr

**Example**:
```bash
todo update --id "task-123" --title "Updated title" --priority low
```

### 4. Complete Task
**Command**: `todo complete`

**Parameters**:
- `--id` (required, str): Task ID to update
- `--status` (optional, bool): Completion status (default: true)

**Response**:
- Success: "Task marked as {completed/incomplete}"
- Error: Error message to stderr

**Example**:
```bash
todo complete --id "task-123" --status true
```

### 5. Delete Task
**Command**: `todo delete`

**Parameters**:
- `--id` (required, str): Task ID to delete

**Response**:
- Success: "Task deleted successfully"
- Error: Error message to stderr

**Example**:
```bash
todo delete --id "task-123"
```

## Error Handling

### Standard Error Responses
- `TASK_NOT_FOUND`: "Error: Task with ID {id} not found"
- `INVALID_INPUT`: "Error: Invalid input - {details}"
- `DUPLICATE_TAG`: "Error: Duplicate tags detected"
- `MISSING_REQUIRED_FIELD`: "Error: Missing required field - {field}"

### Exit Codes
- `0`: Success
- `1`: General error
- `2`: Usage error (incorrect command usage)
- `3`: Resource not found error

## Data Formats

### Task Representation (Output)
```
ID: {id}
Title: {title}
Description: {description or "None"}
Priority: {priority}
Tags: {comma-separated tags or "None"}
Status: {completed/incomplete}
Created: {ISO datetime}
```

### Task List (Output)
Formatted table with columns: ID, Title, Status, Priority, Tags, Created