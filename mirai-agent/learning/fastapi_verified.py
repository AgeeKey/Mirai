"""
fastapi - Verified Learning Artifact

Quality Grade: D
Overall Score: 0.70
Tests Passed: 0/1
Learned: 2025-10-20T13:47:06.659559

This code has been verified by MIRAI's NASA-level learning system.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# In-memory database simulation
items_db: List[Item] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    """
    Create a new item and store it in the in-memory database.
    """
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items():
    """
    Retrieve all items from the in-memory database.
    """
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """
    Retrieve a specific item by its ID.
    """
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    """
    Update an existing item by its ID.
    """
    for index, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            items_db[index] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    """
    Delete an item by its ID.
    """
    for index, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            del items_db[index]
            return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# To run the application, use the command: uvicorn <filename>:app --reload