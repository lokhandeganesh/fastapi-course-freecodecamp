from fastapi import APIRouter, status, HTTPException
from fastapi import Depends


# Sqlalchemy imports
from app.database import get_db
from sqlalchemy.orm import Session

from app.model import models
from app.schema import schemas

# Implementing Argon2 password hashing
from app.utils_folder import utils

from app.logging.logger import logger

router = APIRouter(
	prefix="/course_auth",
	tags=['Course Authentication']
)

# (Authentication routes can be added here in the future)
@router.post("/login")
async def course_login(user_credentials:schemas.UserLogin, db: Session = Depends(get_db)):
	# query the database to find user by email
	user = db.query(models.UserJWT).filter(models.UserJWT.email == user_credentials.email).first()

	if not user:
		logger.warning(f"User Account does not exist: {user_credentials.email}")
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Invalid Credentials"
		)

	# check if password matches
	if not utils.verify_password(user.password, user_credentials.password):
		logger.warning(f"Login failed for email: {user_credentials.email}")
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Invalid Credentials"
		)

	logger.info(f"User logged in with email: {user_credentials.email}")
	# create and return a token (dummy token for now)
	return {"token" : "dummy_token"}
