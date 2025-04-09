# Task Manager API
Backend API for managing user tasks, built with FastAPI, JWT auth, and SQLAlchemy with PostgreSQL.

## Features
- User signup/login with JWT (30-min tokens)
- Create, read, update, delete tasks (title, description, status, priority, deadline)
- Task ownership enforced via `user_id` checks
- PostgreSQL database for persistent storage

## Deployment
- Hosted on Render: [https://task-manager-api-5wzd.onrender.com](https://task-manager-api-5wzd.onrender.com)
- API is publicly accessible with endpoints under `/auth` and `/task` prefixes

## Run Locally
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file:

SECRET_KEY=your-secret-key

ALGORITHM=your-algorithm

ADMIN_KEY=your-admin-key

DATABASE_URL=postgresql://user:password@localhost:5432/task_manager

*Note:* Replace `user`, `password`, and database name with your local PostgreSQL credentials.
4. Run the application: `uvicorn main:app --reload`

## API Endpoints
- **Auth**
- `POST /auth/user/signup` - Register a new user
- `POST /auth/user/login` - Login and receive JWT
- `GET /auth/user/ViewAll` - List all users (admin only)
- **Tasks**
- `GET /task` - List all tasks for authenticated user
- `POST /task/create` - Create a new task
- `PUT /task/update/{id}` - Update a task
- `DELETE /task/delete/{id}` - Delete a task

## Notes
- Uses PostgreSQL as the database, configured via the `DATABASE_URL` environment variable
- JWT tokens expire after 30 minutes
- Admin access requires the `ADMIN_KEY` environment variable
- Ensure PostgreSQL is installed and running locally for development