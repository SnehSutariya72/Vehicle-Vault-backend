from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from bson import ObjectId
from models.CarDetailsModel import CarDetailsModel

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.vehicle_db
cars_collection = db.cars
car_details_collection = db.car_details

class CarDetailsController:
    @staticmethod
    async def add_car_details(car_id: str, details: dict) -> CarDetailsModel:
        try:
            print(f"🔍 Checking Car ID: {car_id}")  # Debug log
            existing_details = await car_details_collection.find_one({"car_id": car_id})

            if existing_details:
                print("ℹ️ Updating existing car details")  # Debug log
                await car_details_collection.update_one(
                    {"car_id": car_id}, {"$set": details}
                )
            else:
                print("➕ Adding new car details")  # Debug log
                details["car_id"] = car_id
                await car_details_collection.insert_one(details)

            updated_details = await car_details_collection.find_one({"car_id": car_id})
            if updated_details:
                updated_details.pop("_id", None)  # Remove MongoDB's _id field

            return CarDetailsModel(**updated_details)

        except Exception as e:
            print(f"💥 Unexpected Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_car_details(car_id: str) -> dict:
        try:
            print(f"🔍 Fetching Car ID: {car_id}")
            if not ObjectId.is_valid(car_id):
                print("❌ Invalid Car ID format!")
                raise HTTPException(status_code=400, detail="Invalid Car ID format")

            # Fetch basic car info from cars collection
            car_data = await cars_collection.find_one({"_id": ObjectId(car_id)})
            if not car_data:
                print("❌ Car not found!")
                raise HTTPException(status_code=404, detail="Car not found")

            car_data["_id"] = str(car_data["_id"])

            # Fetch additional details from car_details collection
            details_data = await car_details_collection.find_one({"car_id": car_id})
            if details_data:
                details_data.pop("_id", None)
                car_data.update(details_data)

            return car_data

        except HTTPException as http_exc:
            print(f"⚠️ FastAPI HTTP Exception: {http_exc.detail}")
            raise http_exc
        except Exception as e:
            print(f"💥 Unexpected Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
