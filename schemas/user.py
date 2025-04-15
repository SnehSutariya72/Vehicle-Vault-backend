from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfileSchema(BaseModel):
    id: str
    full_name: Optional[str] = None
    email: EmailStr
    profile_picture: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class UserUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None