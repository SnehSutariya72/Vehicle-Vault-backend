from models.UserModel import User, UserOut, UserLogin, UserUpdate
from bson import ObjectId
from config.database import user_collection, role_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function to get or create default role
async def get_default_role_id():
    # Look for a default "User" role
    default_role = await role_collection.find_one({"name": "User"})
    if not default_role:
        # Create it if it doesn't exist
        result = await role_collection.insert_one({"name": "User"})
        return result.inserted_id
    return default_role["_id"]

# ✅ Add User with proper password hashing
async def addUser(user: User):
    try:
        # Check if user with the same email already exists
        existing_user = await user_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        
        # Convert user model to dictionary
        user_dict = user.dict()
        
        # Hash the password properly
        try:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            user_dict["password"] = hashed_password.decode('utf-8')  # Store as string
        except Exception as e:
            logger.error(f"Password hashing error: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to hash password")
        
        # Handle role assignment
        if user.role_id:
            try:
                role_id = ObjectId(user.role_id)
                role = await role_collection.find_one({"_id": role_id})
                if not role:
                    # If role doesn't exist, use default
                    user_dict["role_id"] = await get_default_role_id()
                else:
                    user_dict["role_id"] = role_id
            except:
                user_dict["role_id"] = await get_default_role_id()
        else:
            # If no role provided, assign default role
            user_dict["role_id"] = await get_default_role_id()
            
        # Insert user into database
        result = await user_collection.insert_one(user_dict)
        
        logger.info(f"User created successfully with ID: {result.inserted_id}")
        return {
            "message": "User created successfully",
            "user_id": str(result.inserted_id)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

# ✅ Get All Users (simplified)
async def getAllUsers():
    try:
        users = await user_collection.find().to_list(length=None)
        result = []

        for user in users:
            # Convert ID to string and remove password
            user["_id"] = str(user["_id"])
            if "password" in user:
                del user["password"]
            
            # Handle role_id gracefully
            if "role_id" in user and user["role_id"]:
                if isinstance(user["role_id"], ObjectId):
                    user["role_id"] = str(user["role_id"])
                
                # Try to fetch role details
                try:
                    role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})
                    if role:
                        role["_id"] = str(role["_id"])
                        user["role"] = role["name"]
                    else:
                        user["role"] = "Unknown Role"
                except Exception:
                    user["role"] = "Unknown Role"
            else:
                user["role_id"] = None
                user["role"] = "No Role Assigned"

            result.append(user)

        return result
    except Exception as e:
        logger.error(f"Error getting all users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve users: {str(e)}")

# ✅ Get User by ID (simplified)
async def getUserById(user_id: str):
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    try:
        user = await user_collection.find_one({"_id": obj_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert _id to string and remove password
        user["_id"] = str(user["_id"])
        if "password" in user:
            del user["password"]
        
        # Handle role information
        if "role_id" in user and user["role_id"]:
            if isinstance(user["role_id"], ObjectId):
                user["role_id"] = str(user["role_id"])
            
            try:
                role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})
                if role:
                    role["_id"] = str(role["_id"])
                    user["role"] = role["name"]
                else:
                    user["role"] = "Unknown Role"
            except Exception:
                user["role"] = "Unknown Role"
        else:
            user["role_id"] = None
            user["role"] = "No Role Assigned"
            
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error getting user by ID: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")

# ✅ Login User (fixed to handle password issues)
async def loginUser(request: UserLogin):
    try:
        # Find user by email
        foundUser = await user_collection.find_one({"email": request.email})
        if not foundUser:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate password - with better error handling for password verification
        stored_password = foundUser.get("password")
        
        # Check if the password exists
        if not stored_password:
            raise HTTPException(status_code=401, detail="No password set for this user")
            
        try:
            # If stored_password is already hashed (begins with $2b$)
            if stored_password.startswith('$2b$'):
                # Use bcrypt to check the password
                password_match = bcrypt.checkpw(
                    request.password.encode('utf-8'), 
                    stored_password.encode('utf-8')
                )
            else:
                # For plain-text stored passwords (fallback for migration)
                password_match = (request.password == stored_password)
                
                # Upgrade to hashed password for future logins
                if password_match:
                    hashed = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
                    await user_collection.update_one(
                        {"_id": foundUser["_id"]},
                        {"$set": {"password": hashed.decode('utf-8')}}
                    )
                    logger.info(f"Upgraded password hash for user {foundUser['_id']}")
                    
            if not password_match:
                raise HTTPException(status_code=401, detail="Invalid password")
            
        except ValueError as e:
            # Handle bcrypt-specific errors
            logger.error(f"Password verification error: {str(e)}")
            raise HTTPException(status_code=500, detail="Password verification failed - invalid format")
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            raise HTTPException(status_code=500, detail="Password verification failed")

        # Convert ObjectId fields to strings
        foundUser["_id"] = str(foundUser["_id"])
        
        # Handle role_id if it exists
        if "role_id" in foundUser and foundUser["role_id"]:
            if isinstance(foundUser["role_id"], ObjectId):
                foundUser["role_id"] = str(foundUser["role_id"])
            
            # Try to get role information
            try:
                role = await role_collection.find_one({"_id": ObjectId(foundUser["role_id"])})
                if role:
                    role["_id"] = str(role["_id"])
                    foundUser["role"] = role["name"]
                else:
                    foundUser["role"] = "Unknown Role"
            except:
                foundUser["role"] = "Unknown Role"
        else:
            foundUser["role_id"] = None
            foundUser["role"] = "No Role Assigned"

        # Remove password from the response
        if "password" in foundUser:
            del foundUser["password"]
            
        logger.info(f"User {foundUser['_id']} logged in successfully")
        return {
            "message": "Login successful",
            "user": foundUser
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

# ✅ Update User (simplified)
async def updateUser(user_id: str, update_data: dict):
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    try:
        # If password is in update data, hash it
        if "password" in update_data and update_data["password"]:
            try:
                hashed_password = bcrypt.hashpw(
                    update_data["password"].encode('utf-8'), 
                    bcrypt.gensalt()
                )
                update_data["password"] = hashed_password.decode('utf-8')
            except Exception as e:
                logger.error(f"Password hashing error: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to hash password")
        
        # Handle role_id if present
        if "role_id" in update_data and update_data["role_id"]:
            try:
                update_data["role_id"] = ObjectId(update_data["role_id"])
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid role ID format")
        
        # Update user
        result = await user_collection.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            # Check if user exists
            user = await user_collection.find_one({"_id": obj_id})
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            # User exists but no changes were made
            return {"message": "No changes applied to user"}
        
        # Get updated user
        updated_user = await getUserById(user_id)
        
        return {
            "message": "User updated successfully",
            "user": updated_user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

# ✅ Delete User (simplified)
async def deleteUser(user_id: str):
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    try:
        result = await user_collection.delete_one({"_id": obj_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": "User deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")