import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")

settings = Settings()