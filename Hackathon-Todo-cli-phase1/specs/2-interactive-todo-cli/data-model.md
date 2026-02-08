# Data Model: Interactive Todo CLI Interface

## Core Entities

### MenuItem Entity

**Definition**: Represents a selectable option in the interactive menu

**Fields**:
- `id` (str): Unique identifier for the menu item; required
- `title` (str): Display title for the menu item; required
- `description` (str): Brief description of what the menu item does; optional
- `action` (Callable): Function to execute when the menu item is selected; required
- `hotkey` (Optional[str]): Keyboard shortcut for the menu item; optional

**Validation Rules**:
- ID must be unique within the menu
- Title must not be empty
- Action must be a callable function

### MenuState Entity

**Definition**: Represents the current state of a menu

**Fields**:
- `current_selection` (int): Index of the currently selected menu item; defaults to 0
- `items` (List[MenuItem]): List of available menu items; defaults to empty list
- `title` (str): Title of the current menu; defaults to "Todo App Menu"

**Validation Rules**:
- Current selection must be within the range of available items
- Items list should not be empty

### SessionState Entity

**Definition**: Represents the overall state of the interactive session

**Fields**:
- `menu_stack` (List[MenuState]): Stack of menu states for navigation history; defaults to empty list
- `should_exit` (bool): Flag indicating if the session should terminate; defaults to False
- `task_service` (TaskService): Reference to the shared task service instance; required

**State Transitions**:
- `running` → `should_exit`: When user selects exit option or presses Esc at main menu
- `should_exit` → `terminated`: When session loop ends

## Data Relationships

### MenuState to MenuItem
- One MenuState contains many MenuItems (1 to many)
- MenuItems are stored as a list within the MenuState entity

### SessionState to MenuState
- One SessionState contains many MenuStates (1 to many)
- MenuStates are stored as a stack for navigation history

### SessionState to TaskService
- One SessionState references one TaskService (1 to 1)
- Provides access to task operations within the session

## In-Memory Storage Model

### Session Storage
- **Storage Mechanism**: In-memory objects (same as existing todo app)
- **Access Pattern**: Direct object reference through SessionState
- **Lifespan**: Exists for the duration of the interactive session
- **Sharing**: Task data is shared between interactive session and any external commands during the same session

## Data Validation

### Input Validation
- Menu item selection: Must be within valid index range
- User inputs for task operations: Same validation as existing todo app
- Keyboard input: Must be valid navigation key (arrows, Enter, Esc, etc.)

### Business Rule Validation
- Cannot navigate to non-existent menu items
- Cannot execute actions on invalid menu selections
- Session state must be properly initialized before use

## Data Access Patterns

### Common Operations
1. Get current menu selection: Access via SessionState → MenuState → current_selection
2. Execute menu action: Retrieve action from MenuItem and call it
3. Navigate menu: Update current_selection in MenuState
4. Push/pop menu states: Manage menu_stack in SessionState