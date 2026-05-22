# Project 3 - Database Integration

A REST API built with Python, Flask and SQLite that performs full CRUD operations with a real database.

## Goal
Connect the backend API to a database to permanently store and retrieve data.

## Tech Stack
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite

## Database Schema

**Table: tasks**

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Auto-generated primary key |
| title | String(100) | Task title (required) |
| description | String(300) | Task description (optional) |
| completed | Boolean | Completion status (default: false) |

## API Endpoints

| Method | Endpoint | Operation | Description |
|--------|----------|-----------|-------------|
| POST | `/tasks` | CREATE | Add a new task |
| GET | `/tasks` | READ | Get all tasks |
| GET | `/tasks/<id>` | READ | Get a single task |
| PUT | `/tasks/<id>` | UPDATE | Update a task |
| DELETE | `/tasks/<id>` | DELETE | Delete a task |

##Key Features
- Full CRUD operations
- Data stored in a persistent SQLite database
- Input validation with meaningful error messages
- Consistent JSON response format
- Database auto-created on first run

##How to Run

1. Install dependencies:
