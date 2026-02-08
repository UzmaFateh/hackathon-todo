# Data Model: AI-Powered Todo Chatbot

## Overview
This document defines the database schema and data models for the AI-Powered Todo Chatbot feature, including conversation history and message storage with proper user isolation.

## Entity: Conversation
Represents a chat session between the user and the AI agent.

### Fields
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `user_id`: UUID (Foreign Key) - Links to the authenticated user (enforces user isolation)
- `title`: String (Optional) - Auto-generated from first message or user-provided
- `created_at`: DateTime - Timestamp when conversation started
- `updated_at`: DateTime - Timestamp when conversation was last updated

### Relationships
- One-to-many with Message entity (one conversation, many messages)
- Many-to-one with User entity (many conversations per user)

### Validation Rules
- `user_id` must exist in users table
- `title` max length 200 characters
- `created_at` and `updated_at` automatically managed by system

### State Transitions
- Created when user starts new conversation
- Updated when new messages are added to the conversation
- Deleted when user deletes conversation (cascades to messages)

## Entity: Message
Represents individual exchanges in a conversation between user and AI.

### Fields
- `id`: UUID (Primary Key) - Unique identifier for the message
- `conversation_id`: UUID (Foreign Key) - Links to parent conversation
- `role`: Enum ('user' | 'assistant') - Identifies who sent the message
- `content`: Text - The actual message content
- `created_at`: DateTime - Timestamp when message was created
- `sequence_number`: Integer - Order of messages within the conversation

### Relationships
- Many-to-one with Conversation entity (many messages per conversation)
- One-to-many with attachments or metadata (future extension)

### Validation Rules
- `role` must be either 'user' or 'assistant'
- `content` max length 10,000 characters
- `sequence_number` must be unique within conversation
- `conversation_id` must exist in conversations table

### State Transitions
- Created when new message is added to conversation
- Never modified after creation (immutable logs)
- Deleted when parent conversation is deleted

## Database Constraints
- Foreign Key: `conversations.user_id` → `users.id` (CASCADE DELETE)
- Foreign Key: `messages.conversation_id` → `conversations.id` (CASCADE DELETE)
- Index: `conversations(user_id)` for efficient user-based queries
- Index: `messages(conversation_id, sequence_number)` for ordered message retrieval
- Composite Unique: `conversations(id, user_id)` to prevent cross-user access
- Check: `messages.role IN ('user', 'assistant')` for data integrity

## Security Considerations
- All queries must filter by `user_id` to enforce user isolation
- No direct access to messages without conversation_id and user validation
- Automatic cleanup through CASCADE DELETE when users or conversations are removed
- Input sanitization required for `content` field to prevent injection

## Query Patterns
### Retrieve conversation history for user
```sql
SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC;
```

### Retrieve messages for conversation
```sql
SELECT * FROM messages WHERE conversation_id = ? ORDER BY sequence_number ASC;
```

### Create new conversation
```sql
INSERT INTO conversations (id, user_id, title, created_at, updated_at) VALUES (?, ?, ?, NOW(), NOW());
```

### Add message to conversation
```sql
INSERT INTO messages (id, conversation_id, role, content, created_at, sequence_number)
VALUES (?, ?, ?, ?, NOW(), (SELECT COALESCE(MAX(sequence_number), 0) + 1 FROM messages WHERE conversation_id = ?));
```

## Migration Requirements
- Add conversations table with specified schema
- Add messages table with specified schema
- Ensure proper indexing for performance
- Set up foreign key constraints with cascading rules