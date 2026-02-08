#!/bin/bash

# Todo App Docker Setup Script - Fixed Version

echo "==========================================="
echo "Todo App - Docker Containerization Setup (Fixed)"
echo "==========================================="

echo ""
echo "Checking prerequisites..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "Prerequisites met. Building and starting containers..."
echo ""

# Build and start the containers with fixed dependencies
echo "Building containers (this may take a few minutes)..."
docker-compose build

echo ""
echo "Starting containers..."
docker-compose up

echo ""
echo "==========================================="
echo "Containers have been stopped."
echo "To start again, run: docker-compose up"
echo "To start in background: docker-compose up -d"
echo "==========================================="