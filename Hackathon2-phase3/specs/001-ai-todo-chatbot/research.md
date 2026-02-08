# Research Summary: AI-Powered Todo Chatbot

## Overview
This research document addresses the technical decisions and best practices for implementing the AI-Powered Todo Chatbot feature, focusing on the key technologies and integration patterns required.

## Decision: OpenAI Agents SDK with Gemini Backend
**Rationale**: Using the `openai-agents-gemini` skill allows us to leverage the OpenAI Agents SDK patterns while using Google's Gemini models via an OpenAI-compatible API adapter. This provides:
- Familiar OpenAI SDK patterns and tool calling mechanisms
- Access to Gemini's advanced reasoning capabilities
- Compatibility with existing OpenAI ecosystem knowledge

**Alternatives considered**:
- Native Gemini SDK: Would require different patterns and tool definitions
- Other LLM providers: Would require different integration patterns
- Custom agent implementation: Would increase complexity and maintenance

## Decision: MCP Python SDK for Todo Operations
**Rationale**: The Model Context Protocol (MCP) provides a standardized way to expose tools to AI agents, offering:
- Clear separation between agent logic and data operations
- Standardized tool discovery and calling mechanisms
- Reusable tool patterns across different agents
- Official SDK support for Python backend integration

**Alternatives considered**:
- Direct API calls from agent: Would violate stateless architecture principles
- Custom tool protocols: Would increase complexity and reduce interoperability
- Function calling without MCP: Would lack standardization

## Decision: Stateless Agent Architecture
**Rationale**: The stateless design is mandated by the constitution and provides:
- Horizontal scalability without shared memory concerns
- Resilience to server restarts
- Clear separation of concerns between agent logic and data persistence
- Predictable behavior and easier debugging

**Implementation approach**:
- Load conversation history from DB on each request
- Process user input with agent
- Store new messages to DB
- Return response to frontend

## Decision: JWT Authentication with User Isolation
**Rationale**: Reusing the existing Better Auth JWT system ensures:
- Consistency with Phase II authentication patterns
- Proper user isolation through validated JWT tokens
- Compliance with security requirements in the constitution

**Implementation approach**:
- Validate JWT token in chat endpoint
- Verify user_id in path matches authenticated user
- Pass current_user to all database operations
- Filter all queries by user_id

## Decision: Neon PostgreSQL with SQLModel
**Rationale**: Building on the existing Phase II database infrastructure provides:
- Consistency with existing data patterns
- Familiar ORM and query patterns
- Neon's serverless scaling capabilities
- Proper transaction support for data integrity

## Best Practices for MCP Tools
**Tool Design Principles**:
- Tools must be pure, synchronous functions
- Tools return clean JSON-serializable dictionaries
- Tools handle their own error cases gracefully
- Tools follow consistent parameter and return value patterns

**Security Considerations**:
- All tools must validate user context and permissions
- Tools must filter operations by user_id
- Input validation within tools for additional security layer

## Best Practices for OpenAI Agents
**Agent Configuration**:
- Detailed system prompt with clear instructions
- Proper tool definitions with comprehensive descriptions
- Error handling and fallback behaviors
- Clarification-seeking behavior for ambiguous requests

**Performance Considerations**:
- Efficient tool calling to minimize LLM interactions
- Proper message history management
- Caching where appropriate (while maintaining statelessness)

## Best Practices for Database Operations
**Data Models**:
- UUID primary keys for security and distributed systems
- Proper foreign key relationships for data integrity
- Timestamps for audit and ordering purposes
- Sequence numbers for message ordering within conversations

**Security**:
- All queries must include user_id filters
- Input sanitization at the application level
- Proper transaction management for consistency
- Connection pooling for performance

## Integration Patterns
**Frontend-Backend**:
- REST API with JWT authentication
- OpenAPI contract for API documentation
- Error handling with user-friendly messages
- Loading states and proper UX feedback

**Agent-Database**:
- Dependency injection for database sessions
- Async/await patterns throughout
- Proper error propagation from tools to agent
- Consistent data validation at all levels