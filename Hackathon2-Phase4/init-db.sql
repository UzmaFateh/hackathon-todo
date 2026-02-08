-- Database initialization script for Todo App

-- Create the database if it doesn't exist
SELECT 'CREATE DATABASE todoapp' WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'todoapp'
);

-- Connect to the todoapp database
\c todoapp;

-- Enable extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Additional initialization commands can be added here if needed
-- For example, creating initial tables, roles, etc.

-- Create a dedicated application user (optional)
-- CREATE USER todo_user WITH PASSWORD 'todo_password';
-- GRANT ALL PRIVILEGES ON DATABASE todoapp TO todo_user;