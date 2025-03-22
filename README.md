# Task Manager API
Backend API for managing user tasks, built with FastAPI, JWT auth, and SQLAlchemy (SQLite).

## Features
- User signup/login with JWT (30-min tokens, `user_id` in payload)
- Create, read, update, delete tasks (title, description, status, priority, deadline)
- Task ownership enforced via `user_id` checks
- SQLite DB with user-task relationships

## Run It
- Install: `pip install -r requirements.txt`
- Run: `uvicorn main:app --reload`
