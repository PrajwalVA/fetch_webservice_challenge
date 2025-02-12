from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel, Field # type: ignore
from typing import List, Dict
import uuid
from datetime import date, time
from math import ceil

app = FastAPI()

user_db: Dict[int, int] = {}
receipts_db: Dict[str, dict] = {}

# Receipt and Item Models (patterns taken from api.yml)

class Item(BaseModel):
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$")
    price: str = Field(..., pattern=r"^[\d+\.\d{2}]+$")

class Receipt(BaseModel):
    retailer: str = Field(..., pattern=r"^[\w\s\-&]+$")
    purchaseDate: date
    purchaseTime: time
    items: List[Item]
    total: str = Field(..., pattern=r"^\d+\.\d{2}$")
    user: int
    points: int = 0

def calculate_points(receipt: Receipt, receipt_count: int) -> int:
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

    if receipt_count == 1:
        points += 1000
    if receipt_count == 2:
        points+=500
    if receipt_count >= 3:
        points+=250

    return points


# @app.get("/receipts/{id}/users")
# async def get_user(id: str):
#     receipt = receipts_db.get(id)
#     if not receipt:
#         raise HTTPException(status_code=404, detail=f"No receipt for {id}")
#     return {"points": receipt.user}

# #POST
# @app.post("/receipts/{id}/users")
# async def user_record(receipt: Receipt):
#     if user_id not in user_db:
#         user_id = str(uuid.uuid4())
#         receipts = list(receipt)
#         user_db[user_id] = receipts
#     else:
#         get_user()
#         receipts = user_db.get(user_id)
#         receipts.add(receipt)
#         user_db[user_id] = receipts


#POST
@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    receipt_count = user_db.get(receipt.user, 1)
    receipt.points = calculate_points(receipt, receipt_count)
    user_db[receipt.user] = receipt_count + 1
    receipts_db[receipt_id] = receipt
    return {"id": receipt_id}

#GET
@app.get("/receipts/{id}/points")
async def get_points(id: str):
    receipt = receipts_db.get(id)
    if not receipt:
        raise HTTPException(status_code=404, detail=f"No receipt for {id}")
    return {"points": receipt.points}