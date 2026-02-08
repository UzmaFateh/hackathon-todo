# OpenAI ChatKit Skill

This skill provides guidance and tools for implementing OpenAI ChatKit features, including managing chat sessions and threads.

## Components

- `SKILL.md`: Main skill definition with API documentation and implementation guidance
- `references/api-reference.md`: Detailed API reference for OpenAI ChatKit endpoints
- `scripts/chatkit-helper.sh`: Command-line helper script for common operations

## Usage

The skill provides guidance for:

1. Creating and managing chat sessions
2. Creating and organizing conversation threads
3. Retrieving session and thread information
4. Implementing best practices for chat applications

## Requirements

- OpenAI API key (set as `OPENAI_API_KEY` environment variable)
- cURL for API calls
- jq for JSON processing (in the helper script)

## Helper Script Commands

```bash
# Create a new session
./scripts/chatkit-helper.sh create-session '{"user_id": "123"}'

# Create a new thread in a session
./scripts/chatkit-helper.sh create-thread "sess_abc123" '{"topic": "support"}'

# List threads in a session
./scripts/chatkit-helper.sh list-threads "sess_abc123"

# Get session details
./scripts/chatkit-helper.sh get-session "sess_abc123"
```