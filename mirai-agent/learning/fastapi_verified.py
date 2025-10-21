"""
fastapi - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.71
Tests Passed: 0/1
Learned: 2025-10-21T10:17:52.982557

This code has been verified by MIRAI's NASA-level learning system.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Define a data model for an item
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
    Create a new item in the database.
    """
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items():
    """
    Retrieve all items from the database.
    """
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """
    Retrieve an item by its ID.
    """
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    """
    Update an existing item by its ID.
    """
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    """
    Delete an item by its ID.
    """
    for index, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[index]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# To run the application, use the command: uvicorn filename:app --reload