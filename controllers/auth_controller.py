from config.database import user_collection
from passlib.context import CryptContext
from schemas.user import UserSignup, UserLogin  # Ensure this path exists
from fastapi import HTTPException
from bson import ObjectId
from jose import jwt, JWTError
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Secret key & algorithm from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to generate JWT token
def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Signup function
async def signup_user(user_data: UserSignup):
    existing_user = await user_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    new_user = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_password
    }
    result = await user_collection.insert_one(new_user)
    return {"message": "User registered successfully!", "user_id": str(result.inserted_id)}

# Login function
async def login_user(user_data: UserLogin):
    user = await user_collection.find_one({"email": user_data.email})
    
    # Check if user exists and password is correct
    if not user or not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        # Generate JWT token
        access_token = create_access_token({"user_id": str(user["_id"]), "email": user["email"]})
    except JWTError:
        raise HTTPException(status_code=500, detail="Token generation failed")
    
    return {
        "message": "Login successful!",
        "user_id": str(user["_id"]),
        "access_token": access_token
    }