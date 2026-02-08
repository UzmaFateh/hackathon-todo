# Quickstart Guide: Interactive Todo CLI Interface

## Prerequisites

- Python 3.13 or higher
- uv package manager
- Rich and Textual libraries installed

## Setup

### 1. Install Dependencies

```bash
# Install Rich and Textual for interactive interface
uv pip install rich textual
```

### 2. Project Structure

```
todo-app/
├── todo/
│   ├── interactive/
│   │   ├── __init__.py
│   │   ├── main.py         # Interactive CLI entry point
│   │   ├── menu.py         # Menu system
│   │   ├── session.py      # Session management
│   │   ├── ui_components.py # UI components
│   │   └── controllers.py  # Menu controllers
│   ├── models/
│   │   └── task.py         # Task data model
│   ├── services/
│   │   └── task_service.py # Business logic
│   └── repositories/
│       └── in_memory_repo.py # Storage
```

## Usage

### Running the Interactive Interface

```bash
# Run the interactive mode directly
python -m todo.interactive.main

# Or if integrated as a mode in the existing app:
todo interactive
```

### Navigation

- **Up Arrow**: Move selection up in menu
- **Down Arrow**: Move selection down in menu
- **Enter**: Execute selected menu item
- **Esc**: Go back to previous menu or exit
- **Q**: Quick exit from main menu

### Menu Options

1. **Add Task**: Prompts for task details and creates a new task
2. **List Tasks**: Shows all tasks with filtering options
3. **Update Task**: Allows updating existing task fields
4. **Complete Task**: Mark tasks as complete/incomplete
5. **Delete Task**: Remove tasks permanently
6. **Exit**: Leave the interactive interface

## Development

### Running Tests

```bash
# Install test dependencies
uv pip install -e ".[dev]"

# Run all tests
python -m pytest

# Run interactive-specific tests
python -m pytest tests/test_interactive.py
```

### Building and Running

```bash
# The interactive application runs in a continuous loop
python -m todo.interactive.main

# Or using the installed command (if integrated)
todo interactive
```

## Configuration

The interactive interface uses the same configuration as the existing todo app:
- All data is stored in-memory only
- Tasks are maintained throughout the interactive session
- Session state is preserved until the interface exits