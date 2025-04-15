from fastapi import APIRouter, HTTPException
from controllers import AreaController  # Import the AreaController
from models.AreaModel import Area, AreaOut  # Import the Area models
from bson import ObjectId
from typing import List

router = APIRouter()

# Route to add a new area
@router.post("/area", response_model=AreaOut)
async def post_area(area: Area):
    return await AreaController.addArea(area)

# Route to get all areas
@router.get("/area", response_model=List[AreaOut])
async def get_area():
    return await AreaController.getArea()

# Route to get a specific area by its ID
@router.get("/area/{area_id}", response_model=AreaOut)
async def get_area_by_id(area_id: str):
    return await AreaController.getAreaById(area_id)

# Route to get all areas by city ID
@router.get("/area/city/{city_id}", response_model=List[AreaOut])
async def get_area_by_city_id(city_id: str):
    return await AreaController.getAreaByCityId(city_id)

# Route to update an area by its ID
@router.put("/area/{area_id}", response_model=AreaOut)
async def update_area(area_id: str, area: Area):
    return await AreaController.updateArea(area_id, area)

# Route to delete an area by its ID
@router.delete("/area/{area_id}")
async def delete_area(area_id: str):
    return await AreaController.deleteArea(area_id)