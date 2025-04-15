from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Profile(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    profile_picture: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None