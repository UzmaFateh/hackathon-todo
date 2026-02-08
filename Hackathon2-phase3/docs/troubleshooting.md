# Troubleshooting Guide: AI Todo Chatbot

## Common Issues and Solutions

### 1. Authentication Issues

**Symptom**: "Unauthorized" or "Invalid token" errors
**Solution**:
- Verify the JWT token is valid and not expired
- Check that the `BETTER_AUTH_SECRET` environment variable matches the one used during token generation
- Ensure the user ID in the path matches the authenticated user

### 2. Chat Agent Not Responding

**Symptom**: Chat requests hang or return no response
**Solution**:
- Check that `GEMINI_API_KEY` environment variable is set correctly
- Verify internet connectivity to the LLM API endpoint
- Check logs for rate limiting errors
- Ensure the MCP server is running if using external tools

### 3. Database Connection Issues

**Symptom**: "Unable to connect to database" or timeout errors
**Solution**:
- Verify `DATABASE_URL` environment variable is set correctly
- Check that the database server is running and accessible
- Ensure the database credentials are correct
- Verify the database has sufficient connections available

### 4. MCP Tools Not Working

**Symptom**: Tool calls fail or return errors
**Solution**:
- Verify the MCP server is running and accessible
- Check that the tool names in the agent configuration match the actual functions
- Look for input validation errors in the tool parameters
- Ensure proper user isolation is maintained in all tools

### 5. Conversation History Not Persisting

**Symptom**: Messages disappear after page refresh
**Solution**:
- Verify the conversation ID is being passed correctly between requests
- Check that the user ID is consistent across requests
- Ensure database transactions are committing properly
- Verify that conversation and message records are being created

### 6. Performance Issues

**Symptom**: Slow response times or timeouts
**Solution**:
- Monitor database query performance
- Check for N+1 query problems in conversation/message retrieval
- Verify the LLM API is responding within expected timeframes
- Consider implementing caching for frequently accessed data

## Debugging Steps

### 1. Enable Verbose Logging
Set `LOG_LEVEL` to `DEBUG` in environment variables to get detailed logs.

### 2. Check Health Endpoints
Access `/health` and `/ready` endpoints to verify service status.

### 3. Verify Environment Variables
Ensure all required environment variables are set:
- `DATABASE_URL`
- `GEMINI_API_KEY`
- `BETTER_AUTH_SECRET`
- `OPENAI_API_KEY`

### 4. Test Database Connectivity
Try connecting to the database directly using the same connection string.

### 5. Test LLM API Connectivity
Verify the LLM API endpoint is accessible and responding to requests.

## Security Issues

### 1. User Isolation Problems
**Issue**: Users can access other users' conversations or tasks
**Solution**:
- Verify all database queries include proper user ID filtering
- Check that path parameters are validated against authenticated user
- Ensure all API endpoints enforce user ID validation

### 2. Input Sanitization Issues
**Issue**: Potential injection attacks
**Solution**:
- Ensure all user inputs are properly sanitized before processing
- Check that message content is validated and filtered
- Verify database queries use parameterized statements

## Monitoring and Health Checks

### 1. API Response Times
Monitor the 95th percentile response time for chat endpoints. Target: <3 seconds.

### 2. Error Rates
Track the percentage of failed requests. Target: <1% error rate.

### 3. LLM API Availability
Monitor connectivity to the LLM API provider. Expected: >99.5% availability.

### 4. Database Health
Monitor database connection pool utilization and query performance.

## Performance Tuning

### 1. Database Indexing
Ensure proper indexes exist on:
- `conversations.user_id`
- `messages.conversation_id`
- `messages.sequence_number`

### 2. Caching Strategy
Consider caching:
- User session information
- Frequently accessed conversations
- Tool response results (if appropriate)

### 3. Connection Pooling
Tune database connection pool size based on expected load.

## Known Limitations

### 1. Rate Limiting
API is limited to 60 requests per minute per user/IP to prevent abuse.

### 2. Message Length
Message content is limited to 10,000 characters to prevent excessive resource usage.

### 3. Conversation History
Large conversation histories may impact performance. Consider implementing pagination.

## Support Resources

For additional support:
- Check application logs in the logging system
- Contact the development team if issues persist
- Review the API documentation for correct usage patterns
- Verify all configuration matches the deployment guide