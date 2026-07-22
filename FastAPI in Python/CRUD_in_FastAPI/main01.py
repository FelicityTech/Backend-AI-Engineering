from fastapi import FastAPI, Depends
from datetime import datetime, timezone
from typing import Any, Annotated, Generic, TypeVar
from contextlib import asynccontextmanager
from fastapi import Request, HTTPException
import random
from pydantic import BaseModel

data : Any = [
    {
        "campaigns_id": 1,
        "name": "Summer Launch",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    },
    {"campaigns_id": 2,
        "name": "Black Friday",
        "due_date": datetime.now(),
        "created_at": datetime.now()
        },
]
@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign.get("campaigns_id") == id:
            return {"campaign": campaign}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.post("/campaigns", status_code=201)
async def create_campaign(body: dict[str, Any]):
    new: Any = {
        "campaigns_id": random.randint(100, 1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()
    }
    data.append(new)
    return {"campaign": new}


@app.put("/campaigns/{id}",)
async def update_campaignid (id: int, body: dict[str, Any]):
    for index, campaign in enumerate(data):
        if campaign.get("campaigns_id") == id:

            updated : Any = {
                "campaigns_id": id, 
                "name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get("created_at")

            }
            data[index] = updated
            return {"campaign": updated}
    raise HTTPException(status_code=404)




@app.delete("/campaigns/{id}",)
async def delete_campaignid (id: int, body: dict[str, Any]):
    for index, campaign in enumerate(data):
        if campaign.get("campaigns_id") == id:
            data.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404)