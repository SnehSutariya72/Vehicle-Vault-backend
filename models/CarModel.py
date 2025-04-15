from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId

class CarModel(BaseModel):
    carId: str = Field(alias="_id")
    make: str
    model: str
    price: float
    color: str
    userId: str
    cityId: str
    kmsDriven: int

    @validator("carId", pre=True, always=True)
    def convert_objectId(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        allow_population_by_field_name = True  # Use _id as carId
        json_encoders = {ObjectId: str}
