from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_db_and_tables
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Task API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0.0",
        "docs": "/docs"
    }


app.include_router(router)
