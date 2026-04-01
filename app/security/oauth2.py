from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import jwt
from jwt import PyJWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db_files.config import settings
from app.schema import schemas
from app.model import models
from app.db_files.database import get_db

import uuid

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='course_auth/login')

# Define the IST timezone
IST_TZ = ZoneInfo("Asia/Kolkata")


# Function to create JWT access token
def create_access_token(data: dict):
    # Create a copy of the data dictionary
    to_encode = data.copy()

    # Set the expiration time in IST timezone
    expire = datetime.now(tz=IST_TZ) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add the expiration time to the payload
    to_encode.update({"exp": expire})

    # Encode the JWT token
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Function to verify JWT access token
def verify_access_token(token: str, credentials_exceptions):
    try:
        # Decode the JWT token
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the user_id from the payload
        user_id: uuid.UUID = payload.get("sub")

        if user_id is None:
            raise credentials_exceptions

        # validate the token data format using Pydantic schema
        token_data = schemas.TokenData(id=user_id)
        # return the token data
        return token_data

    except PyJWTError:
        raise credentials_exceptions


# Dependency to get the current user from the token
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
        )

    token_data = verify_access_token(token, credentials_exceptions)

    # Fetch the actual user from DB to ensure they exist
    query = (select(models.UserJWT).where(models.UserJWT.id == token_data.id))
    result = await db.execute(query)
    user = result.scalars().first()

    if user is None:
        raise credentials_exceptions

    # Returns the full User model object
    return user
