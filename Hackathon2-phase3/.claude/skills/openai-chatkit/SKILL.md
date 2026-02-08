---
name: openai-chatkit
description: |
  This skill provides guidance for implementing OpenAI ChatKit features, including managing chat sessions and threads.
  Use when users ask to implement chat functionality using OpenAI's ChatKit APIs for session management, thread creation, and conversation handling.
---

# OpenAI ChatKit Implementation Guide

## Overview

OpenAI ChatKit provides APIs for managing chat sessions and threads, enabling developers to create sophisticated chat applications with persistent conversation history and multi-turn interactions.

## Core Concepts

### Sessions
- Sessions represent a container for multiple conversation threads
- Use `/beta/chatkit/sessions` endpoint to create and manage sessions
- Sessions can contain metadata for user identification and tracking

### Threads
- Threads represent individual conversation threads within a session
- Use `/beta/chatkit/threads` endpoint to create and manage threads
- Threads are associated with a parent session and can contain conversation history

## API Endpoints

### Create Session
```
POST /beta/chatkit/sessions
```
- Creates a new chat session for managing multiple conversation threads
- Optional metadata parameter for custom session data
- Returns session ID for thread creation and management

### Create Thread
```
POST /beta/chatkit/threads
```
- Creates a new thread within a specified chat session
- Requires session_id parameter to associate with parent session
- Optional metadata parameter for thread-specific data

### List Threads
```
GET /beta/chatkit/threads
```
- Retrieves all threads within a specific session
- Requires session_id as query parameter
- Returns array of thread objects with IDs and session associations

### Get Session Details
```
GET /beta/chatkit/sessions/{session_id}
```
- Retrieves detailed information about a specific chat session
- Uses path parameter for session identification
- Returns session metadata and creation timestamp

## Implementation Workflow

### 1. Session Setup
1. Create a new chat session using the sessions endpoint
2. Store the returned session ID for thread creation
3. Add optional metadata for user identification

### 2. Thread Management
1. Create threads within the session using the threads endpoint
2. Associate conversation history with specific threads
3. Use thread IDs to maintain conversation context

### 3. Conversation Handling
1. Retrieve existing threads to continue conversations
2. Create new threads for separate conversation topics
3. Use session-level metadata for user context

## Code Examples

### Creating a Chat Session
```javascript
const createSession = async (metadata = {}) => {
  const response = await fetch('https://api.openai.com/beta/chatkit/sessions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ metadata })
  });

  return await response.json();
};
```

### Creating a Thread in a Session
```javascript
const createThread = async (sessionId, metadata = {}) => {
  const response = await fetch('https://api.openai.com/beta/chatkit/threads', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      session_id: sessionId,
      metadata
    })
  });

  return await response.json();
};
```

### Listing Threads in a Session
```javascript
const getThreads = async (sessionId) => {
  const response = await fetch(
    `https://api.openai.com/beta/chatkit/threads?session_id=${sessionId}`, {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    }
  );

  return await response.json();
};
```

## Best Practices

1. **Session Management**: Create one session per user or conversation context to organize related threads
2. **Thread Organization**: Use separate threads for different conversation topics within a session
3. **Metadata Usage**: Store user IDs and conversation context in session and thread metadata
4. **Error Handling**: Implement proper error handling for API rate limits and authentication issues
5. **Rate Limiting**: Be mindful of API rate limits when creating multiple sessions or threads

## Security Considerations

- Always use HTTPS for API calls
- Securely store API keys and never expose them in client-side code
- Validate session and thread IDs to prevent unauthorized access
- Implement proper authentication to ensure users can only access their own sessions

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing API integration patterns, authentication methods, and data storage approaches |
| **Conversation** | User's specific chat requirements, session management needs, and thread organization preferences |
| **Skill References** | API patterns from `references/` (session/threads management, error handling) |
| **User Guidelines** | Project-specific conventions, security requirements, and performance expectations |

Ensure all required context is gathered before implementing.