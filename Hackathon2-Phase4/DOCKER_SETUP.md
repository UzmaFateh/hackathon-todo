# Todo App - Docker Containerization

This repository contains a full-stack Todo application with Next.js frontend and FastAPI backend, containerized using Docker.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose installed

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Environment Configuration

Create `.env` files in both the frontend and backend directories with the necessary environment variables:

**backend/.env:**
```
DATABASE_URL=postgresql://user:password@db:5432/todoapp
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_BASE_URL=http://localhost:3001
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**frontend/.env:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 3. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

The application will be accessible at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432

### 4. Alternative: Build Individual Images

To build individual Docker images:

```bash
# Build frontend image
cd frontend
docker build -t todo-frontend .

# Build backend image
cd ../backend
docker build -t todo-backend .
```

## Services

The Docker Compose setup includes:

- **frontend**: Next.js application running on port 3000
- **backend**: FastAPI application running on port 8000
- **db**: PostgreSQL database running on port 5432

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│   Browser   │◄──►│  frontend   │◄──►│    backend   │
│ (Port 3000) │    │(Next.js App)│    │ (FastAPI)    │
└─────────────┘    └─────────────┘    └──────────────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │      db      │
                                        │ (PostgreSQL) │
                                        └──────────────┘
```

## Docker Files

- `Dockerfile` (in frontend/): Multi-stage build for Next.js app
- `Dockerfile` (in backend/): Production-ready Python/FastAPI image
- `docker-compose.yml`: Orchestration of all services
- `.dockerignore`: Files to exclude from Docker builds

## Security Features

- Non-root users in containers for enhanced security
- Proper isolation between services
- Environment variables managed securely
- Health checks for service reliability

## Best Practices Implemented

- Multi-stage builds for optimized images
- Proper dependency layering for efficient caching
- Small base images (alpine variants)
- Proper cleanup of intermediate files
- Secure user permissions inside containers

## Troubleshooting

### Common Issues:

1. **Port already in use**: Make sure ports 3000, 8000, and 5432 aren't being used by other services
2. **Build failures**: Check that all required files are present and accessible
3. **Database connection errors**: Verify environment variables and database initialization

### Useful Commands:

```bash
# View logs
docker-compose logs -f

# View running containers
docker-compose ps

# Stop all services
docker-compose down

# Remove containers, networks, and volumes
docker-compose down -v
```

## Deployment

For production deployment, consider:
- Securing environment variables using Docker secrets
- Using a reverse proxy like nginx
- Setting up SSL certificates
- Configuring resource limits
- Adding monitoring and logging