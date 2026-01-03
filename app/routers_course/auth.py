from fastapi import APIRouter, status, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm


# Sqlalchemy imports
from app.database import get_db
from sqlalchemy.orm import Session

from app.model import models
# from app.schema import schemas

# Implementing Argon2 password hashing
from app.utils_folder import utils
from app.security import oauth

from app.logging.logger import logger

router = APIRouter(
	prefix="/course_auth",
	tags=['Course Authentication']
)

# (Authentication routes can be added here in the future)
@router.post("/login")
async def course_login(
	user_credentials:OAuth2PasswordRequestForm = Depends(),
	db: Session = Depends(get_db)):
	# then request form will return data in the form of
	#  {
	#   "username": "string",
	#   "password": "string"
	#  }

	# query the database to find user by email
	user = db.query(models.UserJWT).filter(
		models.UserJWT.email == user_credentials.username
		).first()

	if not user:
		logger.warning(f"User Account does not exist: {user_credentials.username}")
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Invalid Credentials"
		)

	# check if password matches
	if not utils.verify_password(user.password, user_credentials.password):
		logger.warning(f"Login failed for email: {user_credentials.username}")
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Invalid Credentials"
		)

	logger.info(f"User logged in with email: {user_credentials.username}")

	# Creating a JWT token
	# data that we want to include in the token
	data = {"user_id": user.id}

	# create access token with the data required
	access_token = oauth.create_access_token(data= data)

	return {"access_token" : access_token, "token_type": "bearer"}