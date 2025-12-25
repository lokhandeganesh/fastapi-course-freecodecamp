from fastapi import APIRouter, status, HTTPException

from app.logging.logger import logger

# Sqlalchemy imports
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from app.model import models
from app.schema import schemas

# Implementing Argon2 password hashing
from app.utils_folder import utils

router = APIRouter(
	prefix="/course_users",
	tags=['Course Users']
)

# User Authentication and Authorization
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
async def create_course_users(user:schemas.UserCreate, db:Session = Depends(get_db)):

	# hash the password - user.password
	hashed_password = utils.hash_password(user.password)
	# update the user.password with hashed password
	user.password = hashed_password

	new_user = models.UserJWT(**user.model_dump())

	# add new_post to session
	db.add(new_user)

	try:
		# commit the changes to database
		db.commit()
		# refresh the new_user object to get created in the database
		db.refresh(new_user)

		return new_user

	except IntegrityError as e:
		db.rollback()
		logger.error(f"IntegrityError: {e.orig}")

		if "users_email_key" in str(e.orig):
			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail="User with this email already exists."
			)

		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Could not create user due to data constraint"
		)

@router.get("/{id}", response_model=schemas.UserOut)
def get_course_user(id:int, db:Session = Depends(get_db)):
	user  = db.query(models.UserJWT).filter(models.UserJWT.id ==id).first()

	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"User with id:{id} does not exist."
		)

	return user
