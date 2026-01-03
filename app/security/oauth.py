from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import jwt
from jwt import PyJWTError
from app.config import settings
# from fastapi import Depends, HTTPException, status

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Define the IST timezone
IST_TZ = ZoneInfo("Asia/Kolkata")

def create_access_token(data : dict ):
    # Create a copy of the data dictionary
    to_encode = data.copy()

    # Set the expiration time in IST timezone
    expire = datetime.now(tz=IST_TZ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add the expiration time to the payload
    to_encode.update({"exp": expire})

    # Encode the JWT token
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str, credentials_exceptions):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the user_id from the payload
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exceptions

        return id

    except PyJWTError:
        raise credentials_exceptions
