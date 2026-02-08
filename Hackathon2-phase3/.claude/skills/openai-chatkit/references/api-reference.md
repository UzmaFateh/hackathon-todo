# OpenAI ChatKit API Reference

## API Endpoints Detailed

### POST /beta/chatkit/sessions
Creates a new chat session.

**Request Body:**
- `metadata` (object, optional): Custom metadata for the session (e.g., user_id)

**Response (201):**
- `id` (string): Unique identifier for the session
- `metadata` (object): Session metadata
- `created_at` (string): ISO 8601 timestamp of creation

### POST /beta/chatkit/threads
Creates a new thread within a chat session.

**Request Body:**
- `session_id` (string): Required - The parent session identifier
- `metadata` (object, optional): Custom metadata for the thread (e.g., topic)

**Response (201):**
- `id` (string): Unique identifier for the thread
- `session_id` (string): Parent session identifier
- `metadata` (object): Thread metadata

### GET /beta/chatkit/threads
Lists all threads within a specific session.

**Query Parameters:**
- `session_id` (string): Required - Filter threads by session identifier

**Response (200):**
- `threads` (array): Array of thread objects
  - `id` (string): Thread identifier
  - `session_id` (string): Parent session identifier

### GET /beta/chatkit/sessions/{session_id}
Retrieves detailed information about a specific chat session.

**Path Parameters:**
- `session_id` (string): Required - The unique identifier of the session

**Response (200):**
- `id` (string): Session identifier
- `metadata` (object): Session metadata
- `created_at` (string): ISO 8601 creation timestamp

## Implementation Patterns

### Session-Thread Hierarchy
```
User Session (1)
├── Technical Support Thread (1)
├── Billing Inquiry Thread (2)
└── Feature Request Thread (3)
```

### Context Management
- Store session ID in user's session or JWT token
- Use thread IDs to maintain conversation continuity
- Implement thread cleanup for inactive conversations

## Error Handling

### Common HTTP Status Codes
- 200: Success
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (invalid API key)
- 429: Rate Limited (exceeded API limits)
- 500: Server Error

### Error Response Format
```json
{
  "error": {
    "type": "invalid_request_error",
    "message": "Session ID is required"
  }
}
```

## Rate Limits and Quotas

- Sessions endpoint: 100 requests per minute per API key
- Threads endpoint: 1000 requests per minute per API key
- Implement exponential backoff for rate limit scenarios

## Authentication

- Use Bearer token authentication: `Authorization: Bearer YOUR_API_KEY`
- Store API keys securely in environment variables
- Never expose API keys in client-side code