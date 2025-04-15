from fastapi import APIRouter, Depends, HTTPException
from config.database import db
from models.profile import Profile
from schemas.profile import UserProfile
from auth.auth_utils import get_current_user  # Import token authentication

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=Profile)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Fetch the profile of the currently authenticated user.
    """
    user_email = current_user["email"]  

    profile = db.profiles.find_one({"email": user_email})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return UserProfile(profile)

@router.put("/")
async def update_profile(updated_data: Profile, current_user: dict = Depends(get_current_user)):
    """
    Update the profile of the authenticated user.
    """
    user_email = current_user["email"]
    
    result = db.profiles.update_one({"email": user_email}, {"$set": updated_data.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {"message": "Profile updated successfully"}