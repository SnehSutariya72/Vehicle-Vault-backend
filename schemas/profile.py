from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    full_name: str
    email: str
    profile_picture: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None