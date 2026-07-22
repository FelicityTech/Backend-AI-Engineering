from fastapi import FastAPI, HTTPException

app = FastAPI(title="Task API", 
              version="1.0"
              )

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
        
    raise HTTPException(
        status_code=404, 
        detail={
            "error": f"Task {id} not found"
        }
    )