from fastapi import FastAPI, Depends
from datetime import datetime, timezone
from typing import Any, Annotated, Generic, TypeVar
from contextlib import asynccontextmanager
from fastapi import Request, HTTPException
import random
from pydantic import BaseModel
import sqlite3
from sqlmodel import select, Field, Session, SQLModel, create_engine


class Campaign(SQLModel, table=True):
    campaigns_id: int | None = Field(default=None, primary_key=True)
    name: str =Field(index=True, max_length=100)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True, index=True)

class CampaignCreate(SQLModel):
    name: str
    due_date: datetime | None = Field(default=None, index=True)


sqlite_file_name = "database.db"
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
        if not session.exec(select(Campaign)).first():
            session.add_all([ 
                Campaign(name="Summer Launch", due_date=datetime.now()),
                Campaign(name="Black Friday", due_date=datetime.now())
            ])
            session.commit()
    yield

app = FastAPI(root_path="/api/v1", lifespan=lifespan)
T = TypeVar("T")
class Response(BaseModel, Generic[T]):
    campaigns:T

@app.get("/campaigns", response_model=Response[list[Campaign]])
async def read_campaigns(session: SessionDep):
    data = session.exec(select(Campaign)).all()
    return {"campaigns": data}

@app.get("/campaigns/{campaigns_id}", response_model=Response[Campaign])
async def read_campaign(campaigns_id: int, session: SessionDep):
    data = session.get(Campaign, campaigns_id)

    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"campaigns": data}

@app.post("/campaigns", response_model=Response[Campaign], status_code=201)
async def create_campaign(campaign: CampaignCreate, session: SessionDep):
    db_campaign = Campaign.validate(campaign)
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return {"campaigns": db_campaign}


@app.put("/campaigns/{campaigns_id}", response_model=Response[Campaign])
async def update_campaign(campaigns_id: int, campaign: CampaignCreate, session: SessionDep):
    db_campaign = session.get(Campaign, campaigns_id)
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db_campaign.name = campaign.name
    db_campaign.due_date = campaign.due_date
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return {"campaigns": db_campaign}


@app.delete("/campaigns/{campaigns_id}", status_code=204)
async def delete_campaign(campaigns_id: int, session: SessionDep):
    db_campaign = session.get(Campaign, campaigns_id)
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    session.delete(db_campaign)
    session.commit()
    return None
