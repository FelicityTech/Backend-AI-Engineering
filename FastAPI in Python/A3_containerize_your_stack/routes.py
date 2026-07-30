from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session

from database import get_session
from repository import PostgresTaskRepository
from service import TaskService
from schemas import TaskCreate
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


def get_service(session: Session = Depends(get_session)):
    repository = PostgresTaskRepository(session)
    return TaskService(repository)


@router.get("/")
def get_tasks(service: TaskService = Depends(get_service)):
    return {
        "Tasks": service.get_tasks()
    }


@router.get("/{task_id}")
def get_task(
    task_id: int,
    service: TaskService = Depends(get_service)
):
    task = service.get_task(task_id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Task not found"
            }
        )

    return task


@router.post("/", status_code=201)
def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_service)
):
    return service.create_task(task.title)


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task: TaskCreate,
    service: TaskService = Depends(get_service)
):
    updated = service.update_task(task_id, task.title)

    if updated is None:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Task not found"
            }
        )

    return updated


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_service)
):
    deleted = service.delete_task(task_id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Task not found"
            }
        )

    return {
        "message": f"Task {task_id} deleted"
    }
