import requests

base_url = "http://localhost:8000"
process_url = f"{base_url}/receipts/process"
user_url = f"{base_url}/users"

receipts = [
    {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            },{
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
            },{
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
            },{
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
            },{
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12"
            }
        ],
        "total": "35.35",
        "user": "1"
    },
    {
        "retailer": "Walgreens",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "08:13",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            {"shortDescription": "Dasani", "price": "1.40"}
        ],
        "total": "2.65",
         "user": "1"
    },
    {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {
            "shortDescription": "Gatorade",
            "price": "2.25"
            },{
            "shortDescription": "Gatorade",
            "price": "2.25"
            },{
            "shortDescription": "Gatorade",
            "price": "2.25"
            },{
            "shortDescription": "Gatorade",
            "price": "2.25"
            }
        ],
        "total": "9.00",
        "user": "2"
    },
    {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
        ],
        "total": "1.25",
        "user": "2"
    }
]

receipt_ids = {}

for receipt in receipts:
    response = requests.post(process_url, json=receipt)
    if response.status_code == 200:
        receipt_id = response.json().get("id")
        receipt_ids[receipt_id] = receipt
        print(f"Receipt submitted. ID: {receipt_id}")
    else:
        print(f"Error submitting receipt: {response}")

for receipt_id in receipt_ids:
    points_url = f"{base_url}/receipts/{receipt_id}/points"
    points_response = requests.get(points_url)
    if points_response.status_code == 200:
        points = points_response.json().get("points")
        print(f"Receipt ID: {receipt_id} - Points: {points}")
    else:
        print(f"Error fetching points for receipt {receipt_id}: {points_response}")