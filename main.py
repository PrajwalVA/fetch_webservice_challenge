from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel, Field # type: ignore
from typing import List, Dict
import uuid
from datetime import date, time
from math import ceil

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

def calculate_points(receipt: Receipt) -> int:
    points = 0

    #distinct characters
    points += sum(c.isalnum() for c in receipt.retailer)

    #total based logic
    total_float = float(receipt.total)
    if total_float.is_integer():
        points += 50
    if total_float % 0.25 == 0:
        points += 25

    #items in receipt
    points += (len(receipt.items) // 2) * 5

    #shortDescription length /3 -> points += price * 0.2
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            points += ceil(float(item.price) * 0.2)

    #Day is Odd number 
    if receipt.purchaseDate.day % 2 != 0:
        points += 6

    #Time is between 2 pm and 4 pm
    if 14 <= receipt.purchaseTime.hour < 16:
        points += 10
    
    return points

#POST
@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    receipts_db[receipt_id] = points
    return {"id": receipt_id}

#GET
@app.get("/receipts/{id}/points")
async def get_points(id: str):
    if id not in receipts_db:
        raise HTTPException(status_code=404, detail=f"No receipt for {id}")
    return {"points": receipts_db[id]}