# Data Model: Todo In-Memory Python Console Application

## Core Entities

### Task Entity

**Definition**: The primary entity representing a user's to-do item

**Fields**:
- `id` (str): Stable, unique identifier assigned at creation; required
- `title` (str): Task title; required; min length 1 character
- `description` (Optional[str]): Task description; optional; can be None
- `priority` (Priority): Task priority level; enum with values [HIGH, MEDIUM, LOW]; defaults to MEDIUM
- `tags` (List[str]): List of category labels; optional; defaults to empty list
- `completed` (bool): Completion status; boolean; defaults to False
- `created_at` (datetime): Timestamp of creation; datetime object; defaults to current time

**Validation Rules**:
- Title must not be empty
- Priority must be one of the defined enum values
- Tags must be strings (no special characters restriction initially)
- ID must be unique within the system

**State Transitions**:
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user marks task as incomplete

### Priority Enum

**Definition**: Enumeration for task priority levels

**Values**:
- `HIGH`: Highest priority tasks
- `MEDIUM`: Medium priority tasks (default)
- `LOW`: Lowest priority tasks

### TaskFilter Entity

**Definition**: Criteria for filtering tasks

**Fields**:
- `status` (Optional[str]): Filter by completion status; values [completed, incomplete, all]; optional
- `priority` (Optional[Priority]): Filter by priority level; optional
- `search_term` (Optional[str]): Keyword search across title and description; optional
- `tags` (Optional[List[str]]): Filter by specific tags; optional

## Data Relationships

### Task to Tags
- One Task can have many Tags (0 to many)
- Tags are stored as a list within the Task entity
- Tags are simple string values representing categories

## In-Memory Storage Model

### TaskRepository
- **Storage Mechanism**: Dictionary with task ID as key and Task object as value
- **Indexing**: Primary lookup by task ID (O(1) access)
- **Secondary Indexes**:
  - By completion status (for filtering)
  - By priority (for filtering)
  - By tags (for filtering)

### Storage Lifecycle
- Tasks are created and stored in memory when added
- Tasks remain in memory for the duration of the application session
- Tasks are removed from memory when deleted
- No persistence to external storage (per requirements)

## Data Validation

### Input Validation
- Title: Required, minimum 1 character, maximum 255 characters
- Description: Optional, maximum 1000 characters
- Priority: Must be one of HIGH, MEDIUM, LOW enum values
- Tags: List of strings, each tag maximum 50 characters
- ID: Auto-generated, unique, alphanumeric with hyphens

### Business Rule Validation
- Cannot mark a non-existent task as complete/incomplete
- Cannot update a non-existent task
- Cannot delete a non-existent task
- All operations must be deterministic

## Data Access Patterns

### Common Queries
1. Get all tasks: Retrieve all tasks in the system
2. Get task by ID: Retrieve specific task by unique identifier
3. Filter tasks: Retrieve tasks matching specific criteria
4. Search tasks: Find tasks containing specific keywords

### Performance Considerations
- Primary lookups by ID are O(1) using dictionary
- Filtering operations are O(n) where n is the number of tasks
- For up to 1000 tasks, performance should remain responsive
- Search operations are O(n) as they need to scan content