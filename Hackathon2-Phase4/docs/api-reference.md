# AI Todo Chatbot API Reference

## Overview

The AI Todo Chatbot API provides endpoints for natural language interaction with the todo management system. All endpoints require authentication via JWT token in the Authorization header.

## Authentication

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

## Base URL

```
https://api.example.com/api
```

## Endpoints

### POST /{user_id}/chat

Send a message to the AI chatbot and receive a response.

#### Path Parameters

| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| user_id   | string | The ID of the user (UUID) |

#### Headers

| Header          | Value                  | Description                      |
|-----------------|------------------------|----------------------------------|
| Authorization   | Bearer {token}         | Valid JWT token                  |
| Content-Type    | application/json       | Required for request body        |

#### Request Body

| Field           | Type    | Required | Description                          |
|-----------------|---------|----------|--------------------------------------|
| message         | string  | Yes      | The user's message to the AI agent   |
| conversation_id | string  | No       | The ID of the conversation to continue, or null for new conversation |

#### Response

**Success Response (200)**

```json
{
  "response": "I've added the task 'buy groceries' to your list.",
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "message_id": "987e6543-e21b-32d3-a456-426614174999",
  "success": true
}
```

**Error Responses**

- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or expired JWT token
- `403 Forbidden`: user_id in path does not match authenticated user
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### GET /{user_id}/conversations

Retrieve a list of all conversations for the specified user.

#### Path Parameters

| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| user_id   | string | The ID of the user (UUID) |

#### Headers

| Header          | Value                  | Description                      |
|-----------------|------------------------|----------------------------------|
| Authorization   | Bearer {token}         | Valid JWT token                  |

#### Query Parameters

| Parameter | Type    | Required | Default | Description                     |
|-----------|---------|----------|---------|---------------------------------|
| limit     | integer | No       | 20      | Maximum number of conversations |
| offset    | integer | No       | 0       | Number of conversations to skip |

#### Response

**Success Response (200)**

```json
{
  "conversations": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Grocery planning",
      "created_at": "2023-01-01T12:00:00Z",
      "updated_at": "2023-01-01T15:30:00Z"
    }
  ],
  "total_count": 1
}
```

### GET /{user_id}/conversations/{conversation_id}

Retrieve all messages for a specific conversation.

#### Path Parameters

| Parameter       | Type   | Description                    |
|-----------------|--------|--------------------------------|
| user_id         | string | The ID of the user (UUID)      |
| conversation_id | string | The ID of the conversation (UUID) |

#### Headers

| Header          | Value                  | Description                      |
|-----------------|------------------------|----------------------------------|
| Authorization   | Bearer {token}         | Valid JWT token                  |

#### Response

**Success Response (200)**

```json
{
  "messages": [
    {
      "id": "987e6543-e21b-32d3-a456-426614174999",
      "role": "user",
      "content": "Add a task to buy groceries",
      "created_at": "2023-01-01T12:00:00Z",
      "sequence_number": 1
    }
  ],
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### POST /{user_id}/conversations

Create a new conversation for the user.

#### Path Parameters

| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| user_id   | string | The ID of the user (UUID) |

#### Headers

| Header          | Value                  | Description                      |
|-----------------|------------------------|----------------------------------|
| Authorization   | Bearer {token}         | Valid JWT token                  |
| Content-Type    | application/json       | Required for request body        |

#### Request Body

| Field | Type   | Required | Description                  |
|-------|--------|----------|------------------------------|
| title | string | No       | Optional title for the conversation |

#### Response

**Success Response (201)**

```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2023-01-01T12:00:00Z",
  "title": "New Conversation"
}
```

## Error Codes

| Code | Description                           |
|------|---------------------------------------|
| AUTH_ERROR | Authentication failed              |
| USER_MISMATCH | User ID in path doesn't match token |
| NETWORK_ERROR | Network issue with LLM API         |
| DATABASE_ERROR | Database operation failed          |
| RATE_LIMIT_EXCEEDED | Too many requests              |
| INVALID_INPUT | Invalid request parameters         |

## Rate Limits

The API implements rate limiting to prevent abuse:

- 60 requests per minute per user/IP address
- Excessive requests will return 429 status code