from bson import ObjectId
from fastapi import HTTPException
from typing import List, Dict, Any
import logging
from controllers.CarController import CarController
from models.CarModel import CarModel
from config.database import user_collection, car_collection, role_collection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentController:
    @staticmethod
    async def add_car_by_agent(
        user_id: str, make: str, model: str, price: float,
        color: str, city_id: str, kms_driven: int
    ) -> CarModel:
        try:
            # Validate user exists and has agent role
            try:
                user = await user_collection.find_one({"_id": ObjectId(user_id)})
                if not user:
                    logger.error(f"Agent not found with ID: {user_id}")
                    raise HTTPException(status_code=404, detail="Agent not found")

                # Validate the user's role dynamically from the database
                if "role_id" not in user:
                    logger.error(f"User {user_id} has no role_id")
                    raise HTTPException(status_code=403, detail="User has no role assigned")

                role = await role_collection.find_one({"_id": ObjectId(user.get("role_id"))})
                if not role:
                    logger.error(f"Role not found with ID: {user.get('role_id')}")
                    raise HTTPException(status_code=404, detail="Role not found")
                
                if role.get("name") != "Agent":
                    logger.error(f"User {user_id} has role {role.get('name')}, not Agent")
                    raise HTTPException(status_code=403, detail="User is not authorized to add cars")
            except Exception as e:
                logger.error(f"Error validating user: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Invalid user ID or role: {str(e)}")

            # Create car
            try:
                result = await CarController.create_car_with_details(
                    make=make, model=model, price=price, color=color,
                    userId=user_id, cityId=city_id, kmsDriven=kms_driven
                )
                logger.info(f"Car added successfully: {result}")
                return result
            except Exception as e:
                logger.error(f"Error creating car: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Failed to create car: {str(e)}")
        
        except HTTPException as he:
            # Re-raise HTTP exceptions
            raise he
        except Exception as e:
            # Catch any other exceptions
            logger.error(f"Unexpected error in add_car_by_agent: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    @staticmethod
    async def update_car_by_agent(
        car_id: str, user_id: str, update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            # Validate car ID
            try:
                car_obj_id = ObjectId(car_id)
            except Exception as e:
                logger.error(f"Invalid car ID format: {car_id}")
                raise HTTPException(status_code=400, detail="Invalid car ID format")
            
            # Check if car exists
            car = await car_collection.find_one({"_id": car_obj_id})
            if not car:
                logger.error(f"Car not found with ID: {car_id}")
                raise HTTPException(status_code=404, detail="Car not found")
            
            # Check if user is the owner of the car
            if car.get("userId") != user_id:
                logger.error(f"User {user_id} is not authorized to update car {car_id}")
                raise HTTPException(status_code=403, detail="Not authorized to update this car")
            
            # Validate user exists and has agent role
            try:
                user = await user_collection.find_one({"_id": ObjectId(user_id)})
                if not user:
                    logger.error(f"Agent not found with ID: {user_id}")
                    raise HTTPException(status_code=404, detail="Agent not found")

                role = await role_collection.find_one({"_id": ObjectId(user.get("role_id"))})
                if not role or role.get("name") != "Agent":
                    logger.error(f"User {user_id} is not an agent")
                    raise HTTPException(status_code=403, detail="User is not authorized to update cars")
            except Exception as e:
                logger.error(f"Error validating user: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Invalid user ID or role: {str(e)}")
            
            # Update car
            result = await car_collection.update_one(
                {"_id": car_obj_id},
                {"$set": update_data}
            )
            
            if result.modified_count == 0:
                logger.warning(f"No changes made to car {car_id}")
                # Get current car data even if no changes were made
                updated_car = await car_collection.find_one({"_id": car_obj_id})
                updated_car["_id"] = str(updated_car["_id"])
                return updated_car
            
            # Get updated car data
            updated_car = await car_collection.find_one({"_id": car_obj_id})
            updated_car["_id"] = str(updated_car["_id"])
            logger.info(f"Car {car_id} updated successfully")
            return updated_car
            
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error in update_car_by_agent: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    @staticmethod
    async def get_cars_by_agent(user_id: str) -> List[dict]:
        try:
            try:
                obj_id = ObjectId(user_id)
            except Exception as e:
                logger.error(f"Invalid agent ID format: {user_id}")
                raise HTTPException(status_code=400, detail="Invalid agent ID format")

            # Check if user exists and is an agent
            user = await user_collection.find_one({"_id": obj_id})
            if not user:
                logger.error(f"Agent not found with ID: {user_id}")
                raise HTTPException(status_code=404, detail="Agent not found")

            cars = []
            async for car in car_collection.find({"userId": user_id}):
                car["_id"] = str(car["_id"])
                cars.append(car)
            
            logger.info(f"Found {len(cars)} cars for agent {user_id}")
            return cars
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error in get_cars_by_agent: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    @staticmethod
    async def delete_car_by_agent(car_id: str, user_id: str) -> dict:
        try:
            try:
                car_obj_id = ObjectId(car_id)
            except Exception as e:
                logger.error(f"Invalid car ID format: {car_id}")
                raise HTTPException(status_code=400, detail="Invalid car ID format")

            car = await car_collection.find_one({"_id": car_obj_id})
            if not car:
                logger.error(f"Car not found with ID: {car_id}")
                raise HTTPException(status_code=404, detail="Car not found")

            if car["userId"] != user_id:
                logger.error(f"Unauthorized deletion attempt: User {user_id} tried to delete car {car_id}")
                raise HTTPException(status_code=403, detail="Unauthorized to delete this car")

            result = await car_collection.delete_one({"_id": car_obj_id})
            if result.deleted_count == 1:
                logger.info(f"Car {car_id} deleted successfully by agent {user_id}")
                return {"message": "Car deleted successfully"}

            logger.error(f"Car deletion failed for ID: {car_id}")
            raise HTTPException(status_code=500, detail="Car deletion failed")
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Error in delete_car_by_agent: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")