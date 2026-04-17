from fastapi import Header, HTTPException
from app.config import settings

def verify_token(authorization: str = Header(...)):
    if authorization != f"Bearer {settings.AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")