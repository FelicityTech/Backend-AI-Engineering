# Task API

A RESTful Task Management API built with **FastAPI**, **SQLModel**, and **PostgreSQL** running in **Docker**. The project demonstrates clean architecture by separating business logic from data storage, making it easy to swap repositories without changing the service or API routes.

---

## Features

- Create a task
- Retrieve all tasks
- Retrieve a task by ID
- Update a task
- Delete a task
- PostgreSQL database
- Docker Compose for the complete stack
- Persistent database storage using Docker volumes
- Environment variable configuration with `.env`

---

## Tech Stack

- Python 3.12
- FastAPI
- SQLModel
- PostgreSQL 17
- Docker
- Docker Compose

---

## Project Structure

```
.
├── app/
│   ├── main.py
│   ├── models.py
│   ├── repository.py
│   ├── service.py
│   └── routes.py
├── init.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Architecture

This project follows a layered architecture:

```
Client
   │
   ▼
Routes (FastAPI)
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
PostgreSQL
```

Only the **repository layer** changed when switching from an in-memory store to PostgreSQL.

The service layer and API routes remained unchanged.

---

## Why PostgreSQL?

PostgreSQL was selected because it is:

- Production-ready
- Reliable
- ACID compliant
- Widely used in backend applications
- Fully supported by SQLModel and SQLAlchemy

---

## Why Docker?

Docker makes development consistent by ensuring everyone runs the same versions of Python and PostgreSQL.

Benefits include:

- No local PostgreSQL installation required
- One command starts the entire stack
- Persistent database storage
- Easy setup on any machine

---

## Environment Variables

Create a `.env` file from `.env.example`.

Example:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=tasks

DATABASE_URL=postgresql://postgres:password@db:5432/tasks
```

The `.env` file is ignored by Git.

---

## Running the Project

### Clone the repository

```bash
git clone https://github.com/yourusername/task-api.git

cd task-api
```

### Start the application

```bash
docker compose up --build
```

The first run will:

- Build the FastAPI image
- Download PostgreSQL
- Create the database
- Execute `init.sql`
- Start both services

---

## API Documentation

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | API information |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get a task by ID |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

---

## Persistence

PostgreSQL data is stored in a Docker volume.

Example volume:

```yaml
volumes:
  postgres_data:
```

This means data survives:

- Application restart
- PostgreSQL container restart
- `docker compose down`
- `docker compose up`

(As long as the volume is not removed.)

---

## How Persistence Was Verified

1. Started the application:

```bash
docker compose up
```

2. Created a task using the API.

3. Verified it existed:

```http
GET /tasks
```

4. Stopped the application:

```bash
docker compose down
```

5. Started it again:

```bash
docker compose up
```

6. Retrieved the tasks.

The previously created task was still present, confirming persistent storage.

---

## Database Initialization

The project includes an `init.sql` file that creates the required database schema when PostgreSQL starts for the first time.

---

## Example SQL Query

Retrieve every task:

```sql
SELECT * FROM tasks;
```

Retrieve completed tasks:

```sql
SELECT *
FROM tasks
WHERE done = TRUE;
```

---

## Database Screenshot

Add a screenshot here showing the `tasks` table from your database viewer.

Example:

```
docs/database-viewer.png
```

```markdown
![Database Viewer](docs/database-viewer.png)
```

---

## Docker Services

```yaml
services:
  app:
    ...

  db:
    image: postgres:17
```

Start:

```bash
docker compose up
```

Stop:

```bash
docker compose down
```

---

## Development

Rebuild after changing dependencies:

```bash
docker compose up --build
```

Run containers in the background:

```bash
docker compose up -d
```

View logs:

```bash
docker compose logs -f
```

Stop containers:

```bash
docker compose down
```

Remove everything including volumes:

```bash
docker compose down -v
```

---

## Future Improvements

- User authentication
- Pagination
- Search and filtering
- Unit tests
- Redis caching
- Background jobs
- CI/CD pipeline

---

## License

This project is for educational purposes.
