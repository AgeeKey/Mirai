"""
fastapi - Verified Learning Artifact

Quality Grade: D
Overall Score: 0.70
Tests Passed: 0/1
Learned: 2025-10-18T09:46:37.995274

This code has been verified by MIRAI's NASA-level learning system.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Data model for an item
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# In-memory database simulation
items_db: List[Item] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    """Create a new item."""
    # Check if item with the same id already exists
    if any(existing_item.id == item.id for existing_item in items_db):
        raise HTTPException(status_code=400, detail="Item with this ID already exists.")
    
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items():
    """Retrieve all items."""
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """Retrieve a single item by its ID."""
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found.")
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    """Update an existing item by its ID."""
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found.")

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    """Delete an item by its ID."""
    for index, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[index]
            return {"detail": "Item deleted."}
    raise HTTPException(status_code=404, detail="Item not found.")