from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config.settings import settings
from config.database import db  # Ensure this correctly connects to MongoDB
import logging
from bson import ObjectId

# Setup OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Logging Setup
logging.basicConfig(level=logging.DEBUG)

# Security Settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Extract user from JWT token and validate in MongoDB."""
    logging.debug(f"Received Token: {token}")  # Debug log

    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # 'sub' should store user ID
        logging.debug(f"Decoded User ID: {user_id}")  # Debug log

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: Missing user ID",
            )

        # Fetch user from MongoDB
        user = db.users.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        # Remove sensitive info before returning user data
        user["_id"] = str(user["_id"])
        user.pop("password", None)

        logging.debug(f"Authenticated User: {user}")  # Debug log
        return user

    except JWTError:
        logging.debug("Invalid or Expired Token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    except Exception as e:
        logging.error(f"Unexpected error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )