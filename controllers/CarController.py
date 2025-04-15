from typing import List, Optional
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models.CarModel import CarModel

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.vehicle_db
cars_collection = db.cars

class CarController:
    @staticmethod
    async def create_car(car_data: dict) -> CarModel:
        try:
            result = await cars_collection.insert_one(car_data)
            if result.inserted_id:
                car_data["_id"] = str(result.inserted_id)
                return CarModel(**car_data)
            raise HTTPException(status_code=500, detail="Failed to create car")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def create_car_with_details(
        make: str, model: str, price: float, color: str,
        userId: str, cityId: str, kmsDriven: int
    ) -> CarModel:
        try:
            car_data = {
                "make": make,
                "model": model,
                "price": price,
                "color": color,
                "userId": userId,
                "cityId": cityId,
                "kmsDriven": kmsDriven
            }
            return await CarController.create_car(car_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_cars() -> List[dict]:
        try:
            cars = []
            async for car in cars_collection.find():
                car["_id"] = str(car["_id"])
                cars.append(car)
            return cars
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_car(car_id: str) -> dict:
        try:
            obj_id = ObjectId(car_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid car ID format")

        car = await cars_collection.find_one({"_id": obj_id})
        if car:
            car["_id"] = str(car["_id"])
            return car
        raise HTTPException(status_code=404, detail="Car not found")

    @staticmethod
    async def get_cars_by_user(user_id: str) -> List[dict]:
        try:
            cars = []
            # Log for debugging
            print(f"Looking for cars with userId: {user_id}")
            
            async for car in cars_collection.find({"userId": user_id}):
                car["_id"] = str(car["_id"])
                cars.append(car)
                
            print(f"Found {len(cars)} cars for user {user_id}")
            return cars
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_car(
        car_id: str, make: Optional[str], model: Optional[str], price: Optional[float],
        color: Optional[str], userId: Optional[str], cityId: Optional[str], kmsDriven: Optional[int]
    ) -> dict:
        try:
            obj_id = ObjectId(car_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid car ID format")

        update_data = {}
        if make:
            update_data["make"] = make
        if model:
            update_data["model"] = model
        if price is not None:
            update_data["price"] = price
        if color:
            update_data["color"] = color
        if userId:
            update_data["userId"] = userId
        if cityId:
            update_data["cityId"] = cityId
        if kmsDriven is not None:
            update_data["kmsDriven"] = kmsDriven

        result = await cars_collection.update_one({"_id": obj_id}, {"$set": update_data})
        if result.modified_count > 0:
            updated_car = await cars_collection.find_one({"_id": obj_id})
            updated_car["_id"] = str(updated_car["_id"])
            return updated_car
        raise HTTPException(status_code=404, detail="Car not found or no changes made")

    @staticmethod
    async def delete_car(car_id: str) -> bool:
        try:
            obj_id = ObjectId(car_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid car ID format")

        result = await cars_collection.delete_one({"_id": obj_id})
        if result.deleted_count > 0:
            return True
        raise HTTPException(status_code=404, detail="Car not found")
