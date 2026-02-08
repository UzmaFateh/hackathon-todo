#!/bin/bash
# OpenAI ChatKit Helper Script
# Provides common operations for managing chat sessions and threads

set -e  # Exit on any error

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set"
    echo "Please set your OpenAI API key: export OPENAI_API_KEY=your_key_here"
    exit 1
fi

# Function to create a new chat session
create_session() {
    local metadata="$1"

    echo "Creating new chat session..."

    response=$(curl -s -X POST "https://api.openai.com/beta/chatkit/sessions" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"metadata\": $metadata}")

    session_id=$(echo "$response" | jq -r '.id')

    if [ "$session_id" != "null" ]; then
        echo "Session created successfully!"
        echo "Session ID: $session_id"
        echo "Metadata: $(echo "$response" | jq -r '.metadata')"
        echo "Created at: $(echo "$response" | jq -r '.created_at')"
    else
        echo "Error creating session:"
        echo "$response"
        exit 1
    fi

    echo "$session_id"
}

# Function to create a new thread within a session
create_thread() {
    local session_id="$1"
    local metadata="$2"

    echo "Creating new thread in session: $session_id"

    response=$(curl -s -X POST "https://api.openai.com/beta/chatkit/threads" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"session_id\": \"$session_id\", \"metadata\": $metadata}")

    thread_id=$(echo "$response" | jq -r '.id')

    if [ "$thread_id" != "null" ]; then
        echo "Thread created successfully!"
        echo "Thread ID: $thread_id"
        echo "Session ID: $(echo "$response" | jq -r '.session_id')"
        echo "Metadata: $(echo "$response" | jq -r '.metadata')"
    else
        echo "Error creating thread:"
        echo "$response"
        exit 1
    fi

    echo "$thread_id"
}

# Function to list threads in a session
list_threads() {
    local session_id="$1"

    echo "Listing threads in session: $session_id"

    response=$(curl -s -X GET "https://api.openai.com/beta/chatkit/threads?session_id=$session_id" \
        -H "Authorization: Bearer $OPENAI_API_KEY")

    thread_count=$(echo "$response" | jq -r '.threads | length')

    if [ "$thread_count" -gt 0 ]; then
        echo "Found $thread_count threads:"
        echo "$response" | jq -r '.threads[] | "ID: \(.id), Session: \(.session_id)"'
    else
        echo "No threads found in session $session_id"
    fi
}

# Function to get session details
get_session() {
    local session_id="$1"

    echo "Getting details for session: $session_id"

    response=$(curl -s -X GET "https://api.openai.com/beta/chatkit/sessions/$session_id" \
        -H "Authorization: Bearer $OPENAI_API_KEY")

    if echo "$response" | jq -e '.id' >/dev/null 2>&1; then
        echo "Session details:"
        echo "ID: $(echo "$response" | jq -r '.id')"
        echo "Metadata: $(echo "$response" | jq -r '.metadata')"
        echo "Created at: $(echo "$response" | jq -r '.created_at')"
    else
        echo "Error getting session details:"
        echo "$response"
        exit 1
    fi
}

# Main execution based on command line arguments
case "$1" in
    "create-session")
        metadata="${2:-{}}"
        create_session "$metadata"
        ;;
    "create-thread")
        session_id="$2"
        metadata="${3:-{}}"
        if [ -z "$session_id" ]; then
            echo "Usage: $0 create-thread <session_id> [metadata]"
            exit 1
        fi
        create_thread "$session_id" "$metadata"
        ;;
    "list-threads")
        session_id="$2"
        if [ -z "$session_id" ]; then
            echo "Usage: $0 list-threads <session_id>"
            exit 1
        fi
        list_threads "$session_id"
        ;;
    "get-session")
        session_id="$2"
        if [ -z "$session_id" ]; then
            echo "Usage: $0 get-session <session_id>"
            exit 1
        fi
        get_session "$session_id"
        ;;
    *)
        echo "OpenAI ChatKit Helper Script"
        echo ""
        echo "Usage: $0 <command> [arguments]"
        echo ""
        echo "Commands:"
        echo "  create-session [metadata]    Create a new chat session"
        echo "  create-thread <session_id> [metadata]  Create a new thread in session"
        echo "  list-threads <session_id>    List all threads in a session"
        echo "  get-session <session_id>     Get details of a session"
        echo ""
        echo "Examples:"
        echo "  $0 create-session '{\"user_id\": \"123\"}'"
        echo "  $0 create-thread \"sess_abc123\" '{\"topic\": \"support\"}'"
        echo "  $0 list-threads \"sess_abc123\""
        echo "  $0 get-session \"sess_abc123\""
        ;;
esac