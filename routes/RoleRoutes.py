from fastapi import APIRouter, Body, Path, HTTPException
from typing import Dict, List

from controllers.RoleController import (
    createRole, getAllRoles, assignRoleToUser
)

# Setup router
router = APIRouter()

# ✅ Create Role
@router.post("/create")
async def create_role(role_data: Dict[str, str] = Body(...)):
    """
    Create a new role
    """
    if "name" not in role_data:
        raise HTTPException(status_code=400, detail="Role name is required")
    return await createRole(role_data)

# ✅ Get All Roles
@router.get("/")
async def get_all_roles():
    """
    Retrieve all roles
    """
    return await getAllRoles()

# ✅ Assign Role to User
@router.post("/assign")
async def assign_role(user_id: str = Body(...), role_id: str = Body(...)):
    """
    Assign a role to a user
    """
    return await assignRoleToUser(user_id, role_id)