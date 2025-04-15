from fastapi import APIRouter, Depends, HTTPException
from controllers.UserController import (
    addUser,
    getAllUsers,
    loginUser,
    forgotPassword,
    resetPassword
)
from models.UserModel import User, UserOut, UserLogin, ResetPasswordReq
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config.database import user_collection
from bson import ObjectId
from config.config import SECRET_KEY, ALGORITHM  # Ensure .env is used

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


# Function to get the current logged-in user from the token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Register a new user
@router.post("/user/")
async def post_user(user: User):
    return await addUser(user)


# Fetch all users
@router.get("/users/")
async def get_users():
    return await getAllUsers()


# Login user
@router.post("/user/login/")
async def login_user(user: UserLogin):
    return await loginUser(user)


# Forgot password
@router.post("/user/forgot-password/")
async def forgot_password(email: str):
    return await forgotPassword(email)


# Reset password
@router.post("/user/reset-password/")
async def reset_password(data: ResetPasswordReq):
    return await resetPassword(data)


# Get user profile
@router.get("/user/profile/")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}