from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app = FastAPI(title="Task API", 
              version="1.0"
              )
class TaskCreate(BaseModel):
    title: str | None = None
# In-memory database
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build a REST API",
        "done": False   
    },
    {
        "id": 3,
        "title": "Deploy the API",
        "done": False
    }
]

# Root endpoint
@app.get("/")
async def root():
    data = {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
    return data


# Stage 1 - Health Check
@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


# Get all tasks
@app.get("/tasks")
async def get_tasks():
    return tasks


# GET one task by ID
@app.get("/tasks/{id}")
async def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
        
    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {id} not found"
        }
    )



@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):

    # Validation
    if task.title is None or task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={
                "error": "Task title is required"
            }
        )
    
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)

    return new_task


# Stage 4 - Update and delete task
@app.put("/tasks/{id}")
async def update_task(id: int, task: TaskCreate):
    for i, t in enumerate(tasks):
        if t["id"] == id:
            if task.title is not None:
                tasks[i]["title"] = task.title
            return tasks[i]
    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {id} not found"
        }
    )

@app.delete("/tasks/{id}")
async def delete_task(id: int):
    global tasks
    tasks = [task for task in tasks if task["id"] != id]
    return {"message": f"Task {id} deleted"}