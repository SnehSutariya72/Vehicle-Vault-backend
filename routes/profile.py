from fastapi import APIRouter, Depends, HTTPException, status
from auth.auth_utils import get_current_user  # Make sure this function exists
from schemas.profile import UserProfile
from config.database import db

router = APIRouter()

@router.put("/update", response_model=UserProfile)
async def update_profile(profile_data: UserProfile, user: dict = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    db.users.update_one({"_id": user["_id"]}, {"$set": profile_data.dict()})
    return {"message": "Profile updated successfully"}