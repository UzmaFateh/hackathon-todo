# Quickstart Guide: AI-Powered Todo Chatbot

## Overview
This guide provides the essential information to get started implementing the AI-Powered Todo Chatbot feature, including setup, key components, and development workflow.

## Prerequisites
- Python 3.11+ with pip
- Node.js 18+ with npm/yarn
- Neon PostgreSQL database setup from Phase II
- Better Auth configured for JWT authentication
- OpenAI API key (or equivalent for Gemini adapter)
- MCP Python SDK

## Backend Setup

### 1. Install Dependencies
```bash
cd backend
pip install fastapi uvicorn sqlmodel python-multipart better-exceptions openai-agents python-mcp
```

### 2. Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname"
JWT_SECRET="your-jwt-secret-from-phase-ii"
OPENAI_API_KEY="your-openai-compatible-api-key"
GEMINI_API_KEY="your-gemini-api-key"
```

### 3. Database Models
The conversation and message models should extend the existing SQLModel base:

```python
# backend/models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid
from datetime import datetime

class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200)

class Conversation(ConversationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(back_populates="conversation")

# backend/models/message.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime
from .conversation import Conversation

class MessageBase(SQLModel):
    role: str = Field(regex="^(user|assistant)$")  # Enum-like validation
    content: str = Field(max_length=10000)
    sequence_number: int

class Message(MessageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Conversation = Relationship(back_populates="messages")
```

## MCP Tools Implementation

### 1. Create MCP Server
```python
# backend/mcp/server.py
import asyncio
from mcp.server import Server
from mcp.types import TextContent, ImageContent, Resource, Diagnostic
from pydantic import AnyUrl
from typing import List, AsyncIterator
from .tools import TodoTools

class TodoMcpServer:
    def __init__(self):
        self.server = Server("todo-mcp-server")
        self.todo_tools = TodoTools()

        # Register tools
        self.server.add_tool_handler("add_todo", self.todo_tools.add_todo)
        self.server.add_tool_handler("list_todos", self.todo_tools.list_todos)
        self.server.add_tool_handler("update_todo", self.todo_tools.update_todo)
        self.server.add_tool_handler("complete_todo", self.todo_tools.complete_todo)
        self.server.add_tool_handler("delete_todo", self.todo_tools.delete_todo)

    async def run(self):
        async with self.server.serve_over_stdio():
            await asyncio.Future()  # Run forever
```

### 2. Implement Todo Tools
```python
# backend/mcp/tools.py
from typing import Dict, Any, List
from sqlmodel import Session, select
from models.todo import Todo
from models.user import User
import uuid

class TodoTools:
    def __init__(self):
        # Database session will be injected
        pass

    def add_todo(self, title: str, description: str = "", user_id: str = None) -> Dict[str, Any]:
        """Add a new todo for the user"""
        try:
            # This would be called with a database session
            # Implementation would create a new Todo with user_id
            todo = Todo(
                title=title,
                description=description,
                user_id=uuid.UUID(user_id) if user_id else None
            )
            # Add to database and commit
            return {
                "success": True,
                "todo_id": str(todo.id),
                "message": f"Added todo: {title}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def list_todos(self, user_id: str, status: str = "all") -> Dict[str, Any]:
        """List todos for the user"""
        try:
            # Query todos for user_id with optional status filter
            # Return list of todos
            todos = []  # This would come from DB query
            return {
                "success": True,
                "todos": todos
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # Similar implementations for update_todo, complete_todo, delete_todo
```

## Agent Implementation

### 1. Agent Configuration
```python
# backend/agents/agent_config.py
AGENT_INSTRUCTIONS = """
You are an AI assistant that helps users manage their tasks through natural language.
You must use the provided tools to add, list, update, complete, and delete tasks.
Always ask for clarification if the user's request is ambiguous.
Never create or invent task IDs - only use IDs returned by the tools.
Maintain a helpful and friendly tone.
"""

TOOL_DESCRIPTIONS = {
    "add_todo": {
        "description": "Add a new todo task",
        "parameters": {
            "title": {"type": "string", "description": "The title of the task"},
            "description": {"type": "string", "description": "Optional description of the task"}
        }
    },
    # Similar for other tools
}
```

### 2. Main Agent Logic
```python
# backend/agents/chat_agent.py
from openai import OpenAI
from typing import Dict, Any, List
from .agent_config import AGENT_INSTRUCTIONS, TOOL_DESCRIPTIONS

class ChatAgent:
    def __init__(self, client: OpenAI):
        self.client = client

    def process_message(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Process user message and return agent response"""
        # Prepare the conversation for the LLM
        messages = [
            {"role": "system", "content": AGENT_INSTRUCTIONS},
        ]

        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        # Call the LLM with tool access
        response = self.client.chat.completions.create(
            model="gemini-pro",  # Or appropriate model
            messages=messages,
            tools=self._prepare_tools(),
            tool_choice="auto"
        )

        # Process the response
        return self._process_response(response)

    def _prepare_tools(self):
        """Prepare tools for the LLM"""
        # Convert tool descriptions to OpenAI format
        pass

    def _process_response(self, response):
        """Process the LLM response"""
        # Handle tool calls and format final response
        pass
```

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install @openai/chatkit-react  # Or equivalent for the chat UI
```

### 2. Create Chat Page
```tsx
// frontend/app/chat/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useChat } from './hooks/useChat';
import ChatWindow from './components/ChatWindow';
import NewChatButton from './components/NewChatButton';

export default function ChatPage() {
  const {
    messages,
    sendMessage,
    createNewConversation,
    currentConversationId
  } = useChat();

  return (
    <div className="flex flex-col h-screen">
      <header className="p-4 border-b">
        <h1 className="text-2xl font-bold">AI Todo Assistant</h1>
        <NewChatButton onCreateNew={createNewConversation} />
      </header>

      <main className="flex-1 overflow-y-auto p-4">
        <ChatWindow
          messages={messages}
          onSendMessage={sendMessage}
          currentConversationId={currentConversationId}
        />
      </main>
    </div>
  );
}
```

## Key Implementation Notes

1. **Stateless Design**: The chat endpoint must load conversation history from the database on each request, process the new message, and return the response without storing any state in memory.

2. **User Isolation**: Every database query must filter by the authenticated user's ID to prevent cross-user data access.

3. **MCP Tool Requirements**: MCP tools must be pure, synchronous functions that return JSON-serializable dictionaries.

4. **Error Handling**: The agent must handle tool failures gracefully and return user-friendly messages rather than raw technical errors.

5. **Security**: All user inputs must be validated and sanitized to prevent injection attacks.

## Testing Strategy

1. **Unit Tests**: Test individual components (models, tools, agent logic)
2. **Integration Tests**: Test the full flow from API request to database operations
3. **Contract Tests**: Verify API compliance with the OpenAPI specification
4. **Security Tests**: Validate user isolation and authentication
5. **Performance Tests**: Ensure API latency requirements are met

## Next Steps

1. Implement the data models and database migrations
2. Create the MCP server and tools
3. Build the OpenAI agent with proper tool integration
4. Implement the stateless chat API endpoint
5. Create the frontend chat interface
6. Add comprehensive error handling and validation
7. Perform security and performance testing