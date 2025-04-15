from fastapi import HTTPException
from bson import ObjectId
from config.database import role_collection, user_collection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Create Role
async def createRole(role_data: dict):
    try:
        # Check if role with same name already exists
        existing_role = await role_collection.find_one({"name": role_data["name"]})
        if existing_role:
            return {
                "message": "Role already exists",
                "role_id": str(existing_role["_id"])
            }
        
        # Insert role into database
        result = await role_collection.insert_one(role_data)
        
        logger.info(f"Role created successfully with ID: {result.inserted_id}")
        return {
            "message": "Role created successfully",
            "role_id": str(result.inserted_id)
        }
    except Exception as e:
        logger.error(f"Error creating role: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create role: {str(e)}")

# ✅ Get All Roles
async def getAllRoles():
    try:
        roles = await role_collection.find().to_list(length=None)
        
        # Convert ObjectId to string
        for role in roles:
            role["_id"] = str(role["_id"])
            
        return roles
    except Exception as e:
        logger.error(f"Error getting all roles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve roles: {str(e)}")

# ✅ Assign Role to User
async def assignRoleToUser(user_id: str, role_id: str):
    try:
        # Convert string IDs to ObjectIds
        user_obj_id = ObjectId(user_id)
        role_obj_id = ObjectId(role_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    try:
        # Check if user exists
        user = await user_collection.find_one({"_id": user_obj_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if role exists
        role = await role_collection.find_one({"_id": role_obj_id})
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        # Update user's role
        result = await user_collection.update_one(
            {"_id": user_obj_id},
            {"$set": {"role_id": role_obj_id}}
        )
        
        if result.modified_count == 0:
            # Check if user already has this role
            current_role = user.get("role_id")
            if current_role and str(current_role) == role_id:
                return {"message": f"User already has role: {role['name']}"}
            else:
                raise HTTPException(status_code=500, detail="Failed to assign role")
        
        return {"message": f"Role '{role['name']}' assigned to user successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error assigning role: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to assign role: {str(e)}")