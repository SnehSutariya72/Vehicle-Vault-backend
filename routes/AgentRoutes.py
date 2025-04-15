from fastapi import APIRouter, HTTPException, Form, Depends, Body, Request
from typing import Optional, List, Dict, Any
from fastapi.responses import JSONResponse
from models.CarModel import CarModel
from controllers.AgentController import AgentController
from pydantic import BaseModel

# Remove the prefix here since it's provided in main.py
router = APIRouter(tags=["Agents"])

# Define request models
class AgentCarRequest(BaseModel):
    make: str
    model: str
    price: float
    color: str
    userId: str  # agentId
    cityId: str
    kmsDriven: int

class AgentCarUpdateRequest(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    price: Optional[float] = None
    color: Optional[str] = None
    cityId: Optional[str] = None
    kmsDriven: Optional[int] = None

# ✅ Add Car by Agent - JSON body only
@router.post("/add_car", response_model=CarModel)
async def add_car_by_agent(car_data: AgentCarRequest):
    return await AgentController.add_car_by_agent(
        user_id=car_data.userId,
        make=car_data.make,
        model=car_data.model,
        price=car_data.price,
        color=car_data.color,
        city_id=car_data.cityId,
        kms_driven=car_data.kmsDriven
    )

# ✅ Add Car by Agent - Form data only
@router.post("/add_car_form", response_model=CarModel)
async def add_car_by_agent_form(
    make: str = Form(...),
    model: str = Form(...),
    price: float = Form(...),
    color: str = Form(...),
    userId: str = Form(...),  # agentId
    cityId: str = Form(...),
    kmsDriven: int = Form(...)
):
    return await AgentController.add_car_by_agent(
        user_id=userId,
        make=make,
        model=model,
        price=price,
        color=color,
        city_id=cityId,
        kms_driven=kmsDriven
    )

# ✅ Update Car by Agent - JSON body only
@router.put("/update_car/{car_id}", response_model=CarModel)
async def update_car_by_agent(
    car_id: str,
    user_id: str,
    update_data: AgentCarUpdateRequest
):
    return await AgentController.update_car_by_agent(
        car_id=car_id,
        user_id=user_id,
        update_data=update_data.dict(exclude_none=True)
    )

# ✅ Get All Cars by Agent
@router.get("/cars/{user_id}", response_model=List[CarModel])
async def get_cars_by_agent(user_id: str):
    return await AgentController.get_cars_by_agent(user_id)

# ✅ Delete Car by Agent
@router.delete("/delete_car/{car_id}")
async def delete_car_by_agent(car_id: str, userId: str):
    return await AgentController.delete_car_by_agent(car_id, userId)