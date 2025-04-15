from pydantic import BaseModel, Field
from typing import Optional
import datetime

class Role(BaseModel):
    name: str
    description: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Admin",
                "description": "Administrator role with all privileges"
            }
        }