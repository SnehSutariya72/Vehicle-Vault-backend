from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from bson import ObjectId
from datetime import datetime
from fastapi import File, UploadFile, Form

class Car(BaseModel):
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    variant: Optional[str]
    mileage: Optional[float]
    fuel_type: Optional[str]
    transmission_type: Optional[str]
    price: Optional[float]
    color: Optional[str]
    description: Optional[str]
    status: Optional[str]
    registration_num: Optional[str]
    user_id: Optional[str]
    city_id: Optional[str]
    area_id: Optional[str]
    state_id: Optional[str]
    registration_year: Optional[int]
    insurance: Optional[str]
    seats: Optional[int]
    kms_driven: Optional[float]
    rto: Optional[str]
    ownership: Optional[str]
    engine_displacement: Optional[str]
    no_of_airbags: Optional[int]
    image_url: Optional[str] = None
    image: UploadFile = File(...)  # Accept file for image upload

class CarOut(BaseModel):
    id: str = Field(alias="_id")
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    variant: Optional[str]
    mileage: Optional[float]
    fuel_type: Optional[str]
    transmission_type: Optional[str]
    price: Optional[float]
    color: Optional[str]
    description: Optional[str]
    status: Optional[str]
    registration_num: Optional[str]
    user_id: Optional[str]
    city_id: Optional[str]
    area_id: Optional[str]
    state_id: Optional[str]
    registration_year: Optional[int]
    insurance: Optional[str]
    seats: Optional[int]
    kms_driven: Optional[float]
    rto: Optional[str]
    ownership: Optional[str]
    engine_displacement: Optional[str]
    no_of_airbags: Optional[int]
    image_url: Optional[str] = None
    listing_date: Optional[datetime]
    user: Optional[Dict[str, Any]] = None
    city: Optional[Dict[str, Any]] = None
    area: Optional[Dict[str, Any]] = None
    state: Optional[Dict[str, Any]] = None

    @validator("id", "user_id", "city_id", "area_id", "state_id", pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator("user", "city", "area", "state", pre=True, always=True)
    def convert_nested_objectid(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])  # Convert nested ObjectId to string
        return v