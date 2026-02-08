# Todo In-Memory Python Console Application

A simple command-line todo application that stores tasks in memory.

## Features

- Add tasks with title, description, priority, and tags
- View all tasks with status indicators
- Update existing tasks
- Mark tasks as complete/incomplete
- Delete tasks
- Search and filter tasks
- Interactive menu mode with keyboard navigation

## Important Note

This application stores all data in memory only. Tasks will be lost when the application exits. This is intended for temporary task management within a single session.

## Installation

```bash
pip install todo-app
```

## Usage

### Command Line Mode
```bash
# Add a new task
todo add --title "Buy groceries" --priority high --tags shopping

# List all tasks
todo list

# List only incomplete tasks
todo list --status incomplete

# Update a task
todo update --id <task-id> --title "Updated title"

# Mark a task as complete
todo complete --id <task-id>

# Delete a task
todo delete --id <task-id>
```

### Interactive Mode
```bash
# Run in interactive mode with beautiful menu interface
python -m todo.interactive.main

# The interactive mode provides:
# - Keyboard navigation (arrow keys, Enter, Esc)
# - Visual menu with all task operations
# - Session persistence during the same session
# - Colorful, well-formatted interface
# - Easy task management with guided workflows
```

## Interactive Mode Features

- **Navigation**: Use arrow keys to move up/down, Enter to select, Esc to exit
- **Operations**: Add, List, Update, Complete, Delete tasks
- **Visual Feedback**: Color-coded status indicators and clear formatting
- **Session Persistence**: Tasks created in session remain available during the same session
- **Error Handling**: Clear error messages and validation