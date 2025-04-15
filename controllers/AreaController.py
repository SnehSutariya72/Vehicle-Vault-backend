from models.AreaModel import Area, AreaOut
from bson import ObjectId
from config.database import area_collection, city_collection
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

async def addArea(area: Area):
    # Convert Pydantic model to dictionary and insert into MongoDB
    saved_area = await area_collection.insert_one(area.dict())
    if saved_area.inserted_id:
        return JSONResponse(content={"message": "Area added successfully", "area_id": str(saved_area.inserted_id)}, status_code=201)
    raise HTTPException(status_code=500, detail="Failed to add area")

async def getArea():
    areas = await area_collection.find().to_list(None)
    
    for area in areas:
        # Convert ObjectId to string for foreign keys
        if "city_id" in area and isinstance(area["city_id"], ObjectId):
            area["city_id"] = str(area["city_id"])
        
        # Fetch related city details
        city = await city_collection.find_one({"_id": ObjectId(area["city_id"])})
        if city:
            city["_id"] = str(city["_id"])
            area["city"] = city
    
    return [AreaOut(**area) for area in areas]

async def getAreaById(area_id: str):
    area = await area_collection.find_one({"_id": ObjectId(area_id)})
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    
    # Convert ObjectId to string for foreign keys
    if "city_id" in area and isinstance(area["city_id"], ObjectId):
        area["city_id"] = str(area["city_id"])
    
    # Fetch related city details
    city = await city_collection.find_one({"_id": ObjectId(area["city_id"])})
    if city:
        city["_id"] = str(city["_id"])
        area["city"] = city
    
    return AreaOut(**area)

async def getAreaByCityId(city_id: str):
    areas = await area_collection.find({"city_id": city_id}).to_list(None)
    if not areas:
        raise HTTPException(status_code=404, detail="No areas found for this city")
    
    for area in areas:
        # Convert ObjectId to string for foreign keys
        if "city_id" in area and isinstance(area["city_id"], ObjectId):
            area["city_id"] = str(area["city_id"])
        
        # Fetch related city details
        city = await city_collection.find_one({"_id": ObjectId(area["city_id"])})
        if city:
            city["_id"] = str(city["_id"])
            area["city"] = city
    
    return [AreaOut(**area) for area in areas]

async def updateArea(area_id: str, area: Area):
    updated_area = await area_collection.update_one({"_id": ObjectId(area_id)}, {"$set": area.dict()})
    if updated_area.modified_count > 0:
        return JSONResponse(content={"message": "Area updated successfully"}, status_code=200)
    raise HTTPException(status_code=404, detail="Area not found")

async def deleteArea(area_id: str):
    deleted_area = await area_collection.delete_one({"_id": ObjectId(area_id)})
    if deleted_area.deleted_count > 0:
        return JSONResponse(content={"message": "Area deleted successfully"}, status_code=200)
    raise HTTPException(status_code=404, detail="Area not found")