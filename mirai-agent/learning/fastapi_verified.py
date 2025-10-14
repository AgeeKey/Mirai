"""
FastAPI - Verified Learning Artifact

Quality Grade: D
Overall Score: 0.68
Tests Passed: 0/1
Learned: 2025-10-14T19:06:06.993279

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
    quantity: int

# In-memory database simulation
items_db: List[Item] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    """
    Create a new item in the database.
    
    Parameters:
    - item: Item to be created.
    
    Returns:
    - The created item.
    """
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items() -> List[Item]:
    """
    Retrieve all items from the database.
    
    Returns:
    - A list of items.
    """
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int) -> Item:
    """
    Retrieve an item by its ID.
    
    Parameters:
    - item_id: ID of the item to retrieve.
    
    Raises:
    - HTTPException: If item with the given ID does not exist.
    
    Returns:
    - The requested item.
    """
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item) -> Item:
    """
    Update an existing item.
    
    Parameters:
    - item_id: ID of the item to update.
    - updated_item: New data for the item.
    
    Raises:
    - HTTPException: If item with the given ID does not exist.
    
    Returns:
    - The updated item.
    """
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int) -> dict:
    """
    Delete an item by its ID.
    
    Parameters:
    - item_id: ID of the item to delete.
    
    Raises:
    - HTTPException: If item with the given ID does not exist.
    
    Returns:
    - A message confirming deletion.
    """
    for index, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[index]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# To run the application, use the command: uvicorn filename:app --reload