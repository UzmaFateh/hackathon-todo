#!/bin/bash

# Todo App Docker Setup Script

echo "==========================================="
echo "Todo App - Docker Containerization Setup"
echo "==========================================="

echo ""
echo "Starting Docker containers..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "Building and starting containers..."
echo ""

# Build and start the containers
docker-compose up --build

echo ""
echo "==========================================="
echo "Containers have been stopped."
echo "To start again, run: docker-compose up"
echo "To start in background: docker-compose up -d"
echo "==========================================="