from pydantic import BaseModel
from typing import List, Optional

class CarDetailsModel(BaseModel):
    carId: str
    make: str
    model: str
    price: float
    color: str
    userId: str
    cityId: str
    kmsDriven: int
    description: Optional[str] = None
    features: Optional[List[str]] = []
    accessories: Optional[List[str]] = []
    image: Optional[str] = None  # Added to support image path if provided

    class Config:
        from_attributes = True  # Enables ORM support
