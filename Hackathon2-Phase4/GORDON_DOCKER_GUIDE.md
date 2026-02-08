# Containerizing Your Application with Docker and Gordon AI

This guide covers how to containerize your frontend and backend applications using Docker and Gordon AI, which is an AI assistant for Docker containerization.

## What We've Created

1. **Backend Dockerfile**: A production-ready Dockerfile for your FastAPI backend
2. **Frontend Dockerfile**: A multi-stage build Dockerfile for your Next.js frontend
3. **Docker Compose**: Configuration to orchestrate both services together
4. **Security Enhancements**: Non-root users and health checks
5. **Optimization**: Multi-stage builds and proper layer caching

## Docker Files Created

### Backend Dockerfile (`backend/Dockerfile`)
- Uses Python 3.11-slim base image
- Implements multi-stage build for optimization
- Creates non-root user for security
- Properly handles dependencies with caching

### Frontend Dockerfile (`frontend/Dockerfile`)
- Multi-stage build for optimized production
- Uses Node.js Alpine image
- Implements proper signal handling with dumb-init
- Security best practices with non-root user

### Docker Compose (`docker-compose.yml`)
- Orchestrates frontend, backend, and database services
- Sets up proper networking between services
- Configures environment variables
- Handles service dependencies

## How to Use Gordon AI for Docker (Alternative Approach)

If you want to use Gordon AI to further enhance or modify your Docker setup:

1. **Install Gordon AI** (if not already installed):
   - Gordon is an AI Dockerfile generator that can be accessed online
   - Visit: https://gordon.dock.io/ (or use Docker's AI features)

2. **Using Gordon AI to review or generate Dockerfiles**:
   ```bash
   # Gordon AI can analyze your codebase and suggest improvements
   # You can paste your existing Dockerfiles for optimization

   # Example Gordon command (if installed locally):
   # gordon analyze backend/
   # gordon analyze frontend/
   ```

3. **Gordon AI typically provides:**
   - Optimized base images
   - Layer optimization suggestions
   - Security scanning and recommendations
   - Multi-platform build configurations

## Building and Running

### Quick Start:
```bash
# Make sure you're in the project root directory
# Then run the setup script:
./setup-docker.sh

# Or run directly:
docker-compose up --build
```

### Individual Service Builds:
```bash
# Build only the backend
cd backend
docker build -t todo-backend .

# Build only the frontend
cd ../frontend
docker build -t todo-frontend .
```

### Accessing the Applications:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/health
- Database: localhost:5432 (for external connections)

## Security Considerations Implemented

- **Non-root users**: Both containers run as non-root users
- **Minimal base images**: Using Alpine and slim variants
- **Proper file permissions**: Correct ownership of application files
- **Network isolation**: Services communicate through defined networks

## Optimization Features

- **Multi-stage builds**: Reduces final image size
- **Layer caching**: Optimizes rebuild times by caching dependencies
- **.dockerignore files**: Excludes unnecessary files from builds
- **Health checks**: Monitors container health

## Environment Variables

Both applications are configured to use environment variables:

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@db:5432/todoapp
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_BASE_URL=http://localhost:3001
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Frontend (.env)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Troubleshooting

### Common Issues:

1. **Port conflicts**: Make sure ports 3000, 8000, and 5432 are free
2. **Build cache issues**: Use `docker-compose build --no-cache` if needed
3. **Environment issues**: Verify your .env files are properly configured

### Useful Commands:
```bash
# View logs
docker-compose logs -f

# View container status
docker-compose ps

# Stop containers
docker-compose down

# Clean everything (including volumes)
docker-compose down -v

# Build without cache
docker-compose build --no-cache
```

## Production Considerations

For production deployment, additionally consider:

- SSL/TLS termination with a reverse proxy (nginx)
- Persistent volumes for database data
- Secrets management for sensitive data
- Resource limits and monitoring
- Backup strategies for database
- Health check endpoints in your applications
- CI/CD pipeline integration

## Verification Steps

After running `docker-compose up --build`, verify:

1. ✅ All containers are running: `docker-compose ps`
2. ✅ Frontend is accessible at http://localhost:3000
3. ✅ Backend health check at http://localhost:8000/api/health
4. ✅ Database is connected and initialized
5. ✅ Frontend can communicate with backend API