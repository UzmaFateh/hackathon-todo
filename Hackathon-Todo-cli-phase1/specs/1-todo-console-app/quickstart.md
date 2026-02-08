# Quickstart Guide: Todo In-Memory Python Console Application

## Prerequisites

- Python 3.13 or higher
- uv package manager (latest version)

## Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd todo-app
```

### 2. Install uv (if not already installed)
```bash
pip install uv
```

### 3. Create Virtual Environment
```bash
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4. Install Dependencies
```bash
uv pip install -e .
```

## Project Structure

```
todo-app/
├── pyproject.toml          # Project configuration and dependencies
├── uv.lock                 # Lock file for reproducible builds
├── README.md
├── .python-version         # Specifies Python version (3.13)
├── todo/
│   ├── __init__.py
│   ├── main.py             # Main CLI entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py         # Task data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py # Business logic
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── in_memory_repo.py # In-memory storage
│   └── cli/
│       ├── __init__.py
│       └── commands.py     # CLI command definitions
├── tests/
│   ├── test_models.py      # Model tests
│   ├── test_services.py    # Service tests
│   └── test_cli.py         # CLI tests
```

## Basic Usage

### Add a Task
```bash
# Add a simple task
todo add --title "Buy groceries"

# Add a task with all options
todo add --title "Complete project" --description "Finish the todo app implementation" --priority high --tags work important
```

### List Tasks
```bash
# List all tasks
todo list

# List only incomplete tasks
todo list --status incomplete

# List high priority tasks
todo list --priority high

# Search tasks containing a keyword
todo list --search "groceries"

# Filter by tags
todo list --tags work
```

### Update a Task
```bash
# Update specific fields of a task (use task ID from list command)
todo update --id <task-id> --title "Updated title" --priority low
```

### Mark Task Complete/Incomplete
```bash
# Mark a task as complete
todo complete --id <task-id>

# Mark a task as incomplete
todo complete --id <task-id> --status false
```

### Delete a Task
```bash
# Delete a task by ID
todo delete --id <task-id>
```

## Development

### Running Tests
```bash
# Install test dependencies
uv pip install -e ".[test]"

# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=todo
```

### Adding Dependencies
```bash
# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>
```

### Building and Running
```bash
# The application is run directly via Python
python -m todo.main

# Or using the installed command
todo --help
```

## Configuration

The application uses the following configuration:
- All data is stored in-memory only
- Tasks are automatically assigned UUIDs as IDs
- Default priority is "medium"
- Tasks are sorted by creation date (newest first)