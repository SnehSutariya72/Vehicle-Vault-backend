import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

settings = Settings()