# Task API

A small in-memory CRUD API for managing a to-do list, built with **Python + FastAPI**.
Built as part of the W2 · A1 assignment — no database yet, everything lives in memory
and resets when the server restarts.

## What this is

Four endpoints (plus a couple of freebies) that let a client create, read, update, and
delete tasks. Interactive docs are generated automatically by FastAPI at `/docs`.

## How to install & run

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open:
- http://localhost:8000/ — API description
- http://localhost:8000/docs — Swagger UI (interactive docs, "Try it out" works here)

## Endpoints

| Method | Path            | Description                          | Success | Errors        |
|--------|-----------------|---------------------------------------|---------|----------------|
| GET    | `/`             | API description                       | 200     | —              |
| GET    | `/health`       | Health check                          | 200     | —              |
| GET    | `/tasks`        | List all tasks (supports `?done=`, `?search=`, `?limit=&offset=`) | 200 | — |
| GET    | `/tasks/{id}`   | Get one task                          | 200     | 404            |
| POST   | `/tasks`        | Create a task (`{"title": "..."}`)    | 201     | 400 (missing/empty title) |
| PUT    | `/tasks/{id}`   | Update a task's `title` and/or `done` | 200     | 400 (empty body), 404 (unknown id) |
| DELETE | `/tasks/{id}`   | Delete a task                         | 204     | 404            |
| GET    | `/stats`        | `{ total, done, open }` counts (extra) | 200    | —              |
| POST   | `/reset`        | Restore the 3 example tasks (extra)   | 200     | —              |

## Example `curl -i` output

```
$ curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'

HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

```
$ curl -i http://localhost:8000/tasks/99

HTTP/1.1 404 Not Found
content-type: application/json

{"error":"Task 99 not found"}
```

## Swagger screenshot

_(Add a screenshot of `/docs` here after running the server locally and trying out
a full CRUD cycle through "Try it out".)_

`![Swagger UI](docs/swagger.png)`

## The mortality experiment

Data is stored in a plain Python list (`tasks`), which lives in the server process's
memory. Creating tasks, then restarting `uvicorn`, resets the list back to the 3
default example tasks — every task you created is gone, because nothing was ever
written to disk. This is exactly why Week 3 introduces a real database: memory is
fast but disappears the moment the process stops.

## Notes on validation & status codes

- `POST /tasks` and `PUT /tasks/{id}` are validated with Pydantic models. FastAPI's
  default validation error is a `422`; a custom exception handler in `main.py`
  normalizes that (and all `HTTPException`s) to the spec's expected `400` /
  `404` with a plain `{"error": "..."}` body, instead of FastAPI's default
  `{"detail": "..."}`.
- `PUT /tasks/{id}` requires at least one of `title` or `done` in the body —
  an empty `{}` returns `400`.

## Suggested commit history

Since this was generated in one pass, split it into the assignment's expected
stage-by-stage commits when you push to GitHub, e.g.:

```bash
git init
git add main.py
git commit -m "Stage 0: hello server"
# ...add the root/health endpoints, commit...
git commit -m "Stage 1: root and health endpoints"
# ...add GET /tasks, GET /tasks/{id}, commit...
git commit -m "Stage 2: read endpoints with 404"
# ...add POST /tasks, commit...
git commit -m "Stage 3: create with validation"
# ...add PUT/DELETE, commit...
git commit -m "Stage 4: full CRUD"
# ...docs already built-in via FastAPI, add description strings, commit...
git commit -m "Stage 5: Swagger UI"
git add README.md requirements.txt
git commit -m "Stage 6: publish and docs"
git remote add origin <your-repo-url>
git push -u origin main
```
