from fastapi import APIRouter, Body, Path, HTTPException
from typing import List, Dict, Any
from models.UserModel import User, UserLogin, UserUpdate

# Import controller functions
from controllers.UserController import (
addUser, getAllUsers, getUserById, loginUser, 
    updateUser, deleteUser
)

# Setup router
router = APIRouter()

# ✅ Add new user
@router.post("/", response_model=Dict[str, str])
async def create_user(user: User):
    """
    Create a new user with the provided details
    """
    return await addUser(user)

# ✅ Get all users
@router.get("/")
async def get_all_users():
    """
    Retrieve all users with their details
    """
    return await getAllUsers()

# ✅ Get user by ID
@router.get("/{user_id}")
async def get_user(user_id: str = Path(..., description="The ID of the user to retrieve")):
    """
    Retrieve a specific user by their ID
    """
    return await getUserById(user_id)

# ✅ Login user
@router.post("/login")
async def login_user(login_data: UserLogin):
    """
    Authenticate a user with email and password
    """
    return await loginUser(login_data)

# ✅ Update user
@router.put("/{user_id}")
async def update_user(
    user_data: UserUpdate,
    user_id: str = Path(..., description="The ID of the user to update")
):
    """
    Update user details for a specific user
    """
    # Filter out None values
    update_data = {k: v for k, v in user_data.dict().items() if v is not None}
    return await updateUser(user_id, update_data)

# ✅ Delete user
@router.delete("/{user_id}")
async def delete_user(user_id: str = Path(..., description="The ID of the user to delete")):
    """
    Delete a specific user by their ID
    """
    return await deleteUser(user_id)