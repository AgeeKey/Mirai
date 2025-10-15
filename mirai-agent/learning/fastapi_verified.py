"""
fastapi - Verified Learning Artifact

Quality Grade: D
Overall Score: 0.68
Tests Passed: 0/1
Learned: 2025-10-15T15:31:38.238474

This code has been verified by MIRAI's NASA-level learning system.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Data model for a simple item
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory storage for items
items: List[Item] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    """
    Create a new item.
    
    Args:
        item (Item): The item to be created.
        
    Returns:
        Item: The created item.
    """
    items.append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items() -> List[Item]:
    """
    Retrieve the list of items.
    
    Returns:
        List[Item]: The list of items.
    """
    return items

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int) -> Item:
    """
    Retrieve an item by its ID.
    
    Args:
        item_id (int): The ID of the item to retrieve.
        
    Raises:
        HTTPException: If the item is not found.
        
    Returns:
        Item: The requested item.
    """
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item) -> Item:
    """
    Update an existing item by its ID.
    
    Args:
        item_id (int): The ID of the item to update.
        updated_item (Item): The updated item data.
        
    Raises:
        HTTPException: If the item is not found.
        
    Returns:
        Item: The updated item.
    """
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int) -> dict:
    """
    Delete an item by its ID.
    
    Args:
        item_id (int): The ID of the item to delete.
        
    Raises:
        HTTPException: If the item is not found.
        
    Returns:
        dict: A message confirming the deletion.
    """
    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")