from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel, Field # type: ignore
from typing import List, Dict
import uuid
from datetime import date, time

app = FastAPI()

receipts_db: Dict[str, int] = {}

# Receipt and Item Models (patterns taken from api.yml)
class Item(BaseModel):
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$")
    price: str = Field(..., pattern=r"^\d+\.\d{2}$")

class Receipt(BaseModel):
    retailer: str = Field(..., pattern=r"^[\w\s\-&]+$")
    purchaseDate: date
    purchaseTime: time
    items: List[Item]
    total: str = Field(..., pattern=r"^\d+\.\d{2}$")

#POST
@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    points = 0
    receipts_db[receipt_id] = points
    return {"id": receipt_id}

#GET
@app.get("/receipts/{id}/points")
async def get_points(id: str):
    if id not in receipts_db:
        raise HTTPException(status_code=404, detail=f"No receipt for {id}")
    return {"points": receipts_db[id]}