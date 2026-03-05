from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_DURATION: int = int(os.getenv("ACCESS_TOKEN_DURATION")) 

    ENV: str = os.getenv("ENVIRONMENT", "development")  # default to development if not set


