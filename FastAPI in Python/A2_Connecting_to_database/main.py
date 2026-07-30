from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from typing import Any, Annotated, Generic, TypeVar
from contextlib import asynccontextmanager
from fastapi import Request, HTTPException
import random
from pydantic import BaseModel
import sqlite3
from sqlmodel import select, Field, Session, SQLModel, create_engine




class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=100)
    done: bool = Field(default=False, index=True)


sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Tasks)).first():
            session.add_all([
                Tasks(title="Wake Up", done=True),
                Tasks(title="Brush Teeth", done=True),
                Tasks(title="Take Bath", done= False)
            ])
            session.commit()
    yield

class TaskCreate(BaseModel):
    title: str | None = None
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root(session: SessionDep):
    data = session.exec(select(Tasks)).all()
    return {"Tasks": data}

@app.get("/tasks")
async def read_tasks(session: SessionDep):
    data = session.exec(select(Tasks)).all()
    return {"Tasks": data}


# GET one task by ID
@app.get("/tasks/{id}")
async def get_task(id: int, session: SessionDep):
    task = session.get(Tasks, id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Task not found"
            }
        )

    return task

@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate, session: SessionDep):
    
    # Validation
    if task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={
                "error": "Task title is required"
            }
        )
    
    new_task = Tasks(
        title=task.title,
        done=False
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task