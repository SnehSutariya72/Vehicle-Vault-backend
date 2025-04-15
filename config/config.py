import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get secret key and JWT algorithm
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))