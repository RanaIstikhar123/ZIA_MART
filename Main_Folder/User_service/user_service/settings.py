from starlette.config import Config
from dotenv import load_dotenv
import os
# Load environment variables from .env file
config = Config(".env")


load_dotenv()

# Configuration variables
DATABASE_URL = config("DATABASE_URL", cast=str)
SECRET_KEY = config("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set.")
