import os
from fastapi import UploadFile, File, HTTPException
from config.database import user_collection
from schemas.profile import UserProfile
from uuid import uuid4

UPLOAD_DIR = "uploads/profile_pictures"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_profile_picture(email: str, file: UploadFile):
    # Generate a unique filename
    file_extension = file.filename.split(".")[-1]
    new_filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    # Save file locally
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Update user profile with image URL
    image_url = f"/{UPLOAD_DIR}/{new_filename}"
    result = await user_collection.update_one(
        {"email": email}, {"$set": {"profile_picture": image_url}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Profile picture uploaded", "profile_picture": image_url}

async def update_user_profile(email: str, profile_data: UserProfile):
    existing_user = await user_collection.find_one({"email": email})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {k: v for k, v in profile_data.dict().items() if v is not None}
    
    await user_collection.update_one({"email": email}, {"$set": update_data})
    return {"message": "Profile updated successfully"}