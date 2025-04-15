from fastapi import APIRouter, UploadFile, File, Form
from controllers.CarDetailsController import CarDetailsController

router = APIRouter()

# ✅ POST - Add or Update car details (with optional image upload)
@router.post("/api/car-details/")
async def add_car_details(
    carId: str = Form(...),
    make: str = Form(...),
    model: str = Form(...),
    price: float = Form(...),
    color: str = Form(...),
    userId: str = Form(...),
    cityId: str = Form(...),
    kmsDriven: int = Form(...),
    description: str = Form(None),
    features: str = Form(None),       # comma-separated
    accessories: str = Form(None),    # comma-separated
    image: UploadFile = File(None)
):
    image_url = None
    if image:
        file_location = f"uploads/{image.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(image.file.read())
        image_url = file_location

    details = {
        "carId": carId,
        "make": make,
        "model": model,
        "price": price,
        "color": color,
        "userId": userId,
        "cityId": cityId,
        "kmsDriven": kmsDriven,
        "description": description,
        "features": features.split(",") if features else [],
        "accessories": accessories.split(",") if accessories else [],
        "image": image_url
    }

    return await CarDetailsController.add_car_details(carId, details)


# ✅ GET - Retrieve car details by ID
@router.get("/api/car-details/{car_id}")
async def get_car_details(car_id: str):
    return await CarDetailsController.get_car_details(car_id)
