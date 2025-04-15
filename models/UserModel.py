from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import datetime

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    role_id: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "securepassword",
                "phone": "+1234567890"
            }
        }

class UserOut(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role_id: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "role_id": "60d21b4667d0d8992e610c85",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "securepassword"
            }
        }

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[str] = None
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "phone": "+9876543210"
            }
        }