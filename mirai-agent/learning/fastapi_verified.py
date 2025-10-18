"""
fastapi - Verified Learning Artifact

Quality Grade: D
Overall Score: 0.70
Tests Passed: 1/1
Learned: 2025-10-18T17:12:35.676131

This code has been verified by MIRAI's NASA-level learning system.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Data model for a User
class User(BaseModel):
    id: int
    name: str
    email: str

# In-memory storage for users
users_db: List[User] = []

@app.post("/users/", response_model=User)
async def create_user(user: User) -> User:
    """
    Create a new user and store it in the in-memory database.

    Args:
        user (User): The user data to be created.

    Returns:
        User: The created user.
    """
    # Check if user with the same id already exists
    if any(u.id == user.id for u in users_db):
        raise HTTPException(status_code=400, detail="User with this ID already exists.")
    
    users_db.append(user)  # Add user to the in-memory database
    return user

@app.get("/users/", response_model=List[User])
async def get_users() -> List[User]:
    """
    Retrieve all users from the in-memory database.

    Returns:
        List[User]: A list of all users.
    """
    return users_db  # Return the list of users

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int) -> User:
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Raises:
        HTTPException: If the user is not found.

    Returns:
        User: The requested user.
    """
    user = next((u for u in users_db if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return user  # Return the requested user

@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int) -> User:
    """
    Delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.

    Raises:
        HTTPException: If the user is not found.

    Returns:
        User: The deleted user.
    """
    user = next((u for u in users_db if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    users_db.remove(user)  # Remove the user from the in-memory database
    return user  # Return the deleted user