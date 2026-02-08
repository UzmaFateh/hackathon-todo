# Todo App Usage Guide

## Overview

The Todo In-Memory Python Console Application allows you to manage tasks from the command line. All data is stored in memory only and will be lost when the application exits.

## Commands

### Add a Task

Add a new task with title, description, priority, and tags:

```bash
todo add --title "Task Title" --description "Task description" --priority high --tags work urgent
```

Options:
- `--title` (required): Task title (1-255 characters)
- `--description` (optional): Task description (up to 1000 characters)
- `--priority` (optional): Task priority (high/medium/low, default: medium)
- `--tags` (optional): Task tags (up to 10 tags, max 50 chars each)

### List Tasks

View all tasks with optional filtering:

```bash
todo list
```

Options:
- `--status`: Filter by completion status (completed/incomplete/all)
- `--priority`: Filter by priority (high/medium/low)
- `--search`: Search keyword to match in title/description
- `--tags`: Filter by specific tags

### Update a Task

Update an existing task's fields:

```bash
todo update <task-id> --title "New Title" --priority low
```

Options:
- `task-id` (required): The ID of the task to update
- `--title`: New title
- `--description`: New description
- `--priority`: New priority (high/medium/low)
- `--tags`: New list of tags

### Complete/Incomplete a Task

Mark a task as complete or incomplete:

```bash
todo complete <task-id> --status true
```

Options:
- `task-id` (required): The ID of the task to update
- `--status` (optional): Completion status (true/false, default: true)

### Delete a Task

Remove a task permanently:

```bash
todo delete <task-id>
```

- `task-id` (required): The ID of the task to delete

## Examples

Add a high-priority work task:
```bash
todo add --title "Prepare presentation" --priority high --tags work important
```

List all incomplete tasks:
```bash
todo list --status incomplete
```

Search for tasks containing "grocery":
```bash
todo list --search grocery
```

Mark a task as complete:
```bash
todo complete 123e4567-e89b-12d3-a456-426614174000
```