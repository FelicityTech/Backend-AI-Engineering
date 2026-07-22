"""
Task API — a small CRUD API built with FastAPI.

Run with:
    uvicorn main:app --reload --port 8000

Then visit:
    http://localhost:8000/          -> API description
    http://localhost:8000/health    -> health check
    http://localhost:8000/docs      -> Swagger UI (interactive docs)
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A small in-memory CRUD API for managing a to-do list.",
)

# ---------------------------------------------------------------------------
# Stage 2 — in-memory "database"
# ---------------------------------------------------------------------------

DEFAULT_TASKS = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write README", "done": False},
    {"id": 3, "title": "Ship the API", "done": True},
]

tasks: List[dict] = [dict(t) for t in DEFAULT_TASKS]
next_id = 4


# ---------------------------------------------------------------------------
# Pydantic models (define the shape of request bodies + give us validation)
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="The task's title. Cannot be empty.")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="New title (optional)")
    done: Optional[bool] = Field(None, description="New done state (optional)")


class Task(BaseModel):
    id: int
    title: str
    done: bool


# ---------------------------------------------------------------------------
# Stage 1 — root and health endpoints
# ---------------------------------------------------------------------------

@app.get("/", summary="API description")
def read_root():
    """Returns basic info about this API."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/tasks/{id}", "/health", "/stats", "/reset"],
    }


@app.get("/health", summary="Health check")
def health_check():
    """Simple liveness check — used to confirm the server is up."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Stage 2 — Read
# ---------------------------------------------------------------------------

@app.get("/tasks", response_model=List[Task], summary="List tasks")
def list_tasks(
    done: Optional[bool] = None,
    search: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
):
    """
    Returns all tasks.

    Optional query parameters (extras):
    - done: filter by completion state, e.g. /tasks?done=true
    - search: filter by title substring, e.g. /tasks?search=milk
    - limit / offset: pagination, e.g. /tasks?limit=2&offset=2
    """
    result = tasks

    if done is not None:
        result = [t for t in result if t["done"] == done]

    if search:
        needle = search.lower()
        result = [t for t in result if needle in t["title"].lower()]

    if limit is not None:
        result = result[offset: offset + limit]
    elif offset:
        result = result[offset:]

    return result


@app.get("/tasks/{task_id}", response_model=Task, summary="Get a single task")
def get_task(task_id: int):
    """Returns one task by id, or 404 if it doesn't exist."""
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Stage 3 — Create
# ---------------------------------------------------------------------------

@app.post("/tasks", response_model=Task, status_code=201, summary="Create a task")
def create_task(task: TaskCreate):
    """
    Creates a new task. The client only sends a title; the server assigns
    the id and sets done=false. Empty/missing title -> 400 (handled by
    Pydantic's min_length=1, which FastAPI reports as a 422 by default —
    we normalize that to a plain 400 JSON error below via the exception
    handler).
    """
    global next_id
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task


# ---------------------------------------------------------------------------
# Stage 4 — Update & Delete
# ---------------------------------------------------------------------------

@app.put("/tasks/{task_id}", response_model=Task, summary="Update a task")
def update_task(task_id: int, update: TaskUpdate):
    """
    Replaces a task's title and/or done state.
    - Unknown id -> 404
    - Empty body (no title, no done) -> 400
    """
    if update.title is None and update.done is None:
        raise HTTPException(
            status_code=400,
            detail="Request body must include at least one of: title, done",
        )

    for t in tasks:
        if t["id"] == task_id:
            if update.title is not None:
                t["title"] = update.title
            if update.done is not None:
                t["done"] = update.done
            return t

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    """Removes a task. Returns 204 with no body. Unknown id -> 404."""
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            return JSONResponse(status_code=204, content=None)
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Extras — stats + reset
# ---------------------------------------------------------------------------

@app.get("/stats", summary="Task stats")
def get_stats():
    """Returns counts instead of raw data — the server computing something."""
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    return {"total": total, "done": done, "open": total - done}


@app.post("/reset", summary="Reset to example tasks")
def reset_tasks():
    """Restores the 3 example tasks. Handy for demos and repeated testing."""
    global tasks, next_id
    tasks = [dict(t) for t in DEFAULT_TASKS]
    next_id = 4
    return {"status": "reset", "tasks": tasks}


# ---------------------------------------------------------------------------
# Normalize FastAPI's default validation errors (422) into 400s, so the
# spec's "missing/empty title -> 400" and "invalid body -> 400" hold exactly.
# ---------------------------------------------------------------------------

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    message = "Invalid request body"
    if errors:
        loc = errors[0].get("loc", [])
        field = loc[-1] if loc else "body"
        message = f"Invalid value for '{field}': {errors[0].get('msg')}"
    return JSONResponse(status_code=400, content={"error": message})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Normalize every raised HTTPException (404s, 400s, etc.) to
    # { "error": "..." } instead of FastAPI's default { "detail": "..." }.
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
