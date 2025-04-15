from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from bson import ObjectId

class Area(BaseModel):
    areaName: str
    city_id: str  # Foreign key to City

class AreaOut(Area):
    id: str = Field(alias="_id")
    city: Optional[Dict[str, Any]] = None  # To include city details in the response

    @validator("id", pre=True, always=True)
    def convert_objectId(cls, v):
        if isinstance(v, ObjectId):
            return str(v)  # Convert ObjectId to string
        return v

    @validator("city", pre=True, always=True)
    def convert_city(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])  # Convert city _id to string
        return v