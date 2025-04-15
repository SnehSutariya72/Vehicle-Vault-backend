from fastapi import APIRouter, Depends, HTTPException
from controllers.auth_controller import signup_user, login_user
from schemas.user import UserSignup, UserLogin
from typing import Dict

router = APIRouter(prefix="/auth", tags=["Authentication"])  # Added prefix and tags

@router.post("/signup/")
async def signup(user: UserSignup):
    return await signup_user(user)

@router.post("/login/")
async def login(user: UserLogin):
    return await login_user(user)




