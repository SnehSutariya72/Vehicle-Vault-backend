from fastapi import APIRouter, HTTPException, Form
from typing import Optional, List
from fastapi.responses import JSONResponse
from models.CarModel import CarModel
from controllers.CarController import CarController

router = APIRouter()

# ✅ Create Car
@router.post("/create_car", response_model=CarModel)
async def create_car(
    make: str = Form(...),
    model: str = Form(...),
    price: float = Form(...),
    color: str = Form(...),
    userId: str = Form(...),
    cityId: str = Form(...),
    kmsDriven: int = Form(...)
):
    return await CarController.create_car_with_details(
        make, model, price, color, userId, cityId, kmsDriven
    )

# ✅ Get All Cars
@router.get("/get_cars", response_model=List[CarModel])
async def get_cars():
    return await CarController.get_cars()

# ✅ Get Car by ID
@router.get("/get_car/{car_id}", response_model=CarModel)
async def get_car(car_id: str):
    return await CarController.get_car(car_id)

# ✅ Get Cars by User ID
@router.get("/user/{user_id}", response_model=List[CarModel])
async def get_cars_by_user(user_id: str):
    return await CarController.get_cars_by_user(user_id)

# ✅ Update Car
@router.put("/update_car/{car_id}", response_model=CarModel)
async def update_car(
    car_id: str,
    make: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    color: Optional[str] = Form(None),
    userId: Optional[str] = Form(None),
    cityId: Optional[str] = Form(None),
    kmsDriven: Optional[int] = Form(None)
):
    return await CarController.update_car(
        car_id, make, model, price, color, userId, cityId, kmsDriven
    )

# ✅ Delete Car
@router.delete("/delete_car/{car_id}")
async def delete_car(car_id: str):
    success = await CarController.delete_car(car_id)
    if success:
        return JSONResponse(content={"message": "Car deleted successfully"}, status_code=200)
