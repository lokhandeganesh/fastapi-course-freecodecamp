from fastapi import APIRouter, Response, status, HTTPException
from fastapi import Depends
from typing import List
import uuid

# Sqlalchemy imports
from app.database import get_db
from sqlalchemy.orm import Session

from app.model import models
from app.schema import schemas
from app.security import oauth


from app.logging.logger import logger

router = APIRouter(
	prefix="/course_posts",
	tags=['Course Posts']
)

# Connections from sqlalchemy
@router.get("/", response_model = List[schemas.PostCreateUp])
async def get_course_posts(db:Session = Depends(get_db)):
	posts = db.query(models.PostJWT).all()
	return posts

# post method to create course.post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostCreateUp)
async def create_course_posts(
	post:schemas.PostCreateUp, db:Session = Depends(get_db),
	user_id: uuid.UUID = Depends(oauth.get_current_user)
	):

	print(user_id)

	# print(post.model_dump())
	new_post = models.PostJWT(**post.model_dump())

	# add new_post to session
	db.add(new_post)
	# commit the changes to database
	db.commit()
	# refresh the new_post object to get updated data from database
	db.refresh(new_post)

	return new_post

# to retrive post from posts
@router.get("/{id}")
async def get_course_post(id:int, response: Response, db:Session = Depends(get_db)):
	# query to get post by id
	post = db.query(models.PostJWT).filter(models.PostJWT.id == id).first()

	try:
		if not post:
			logger.info(f"post with id:{id} not found.")

			raise HTTPException(
				status_code = status.HTTP_404_NOT_FOUND,
				detail = f"post with id:{id} not found."
				)
		return post
	except HTTPException:
		# Let FastAPI handle HTTPException (like 404)
		raise
	except Exception as e:
		# Log the exception for debugging
		logger.exception(f"Unhandled error: {e}")

# to delete post from course.posts table
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_course_post(id:int, db:Session = Depends(get_db)):
	# query to delete post by id
	post = db.query(models.PostJWT).filter(models.PostJWT.id == id)

	if not post.first():
		raise HTTPException(
			status_code= status.HTTP_404_NOT_FOUND,
			detail = f"post with id:{id} not found."
		)

	# delete the post
	post.delete(synchronize_session=False)

	# commit the changes to database
	db.commit()

	return Response(status_code=status.HTTP_204_NO_CONTENT)

# to update post from course.posts table
@router.put("/{id}")
async def update_course_post(id:int, post:schemas.PostCreate, db:Session = Depends(get_db)):
	# query to update post by id
	post_query = db.query(models.PostJWT).filter(models.PostJWT.id == id)

	# retrive the post for updating
	updated_post = post_query.first()

	# using index of in posts
	if not updated_post:
		raise HTTPException(
			status_code= status.HTTP_404_NOT_FOUND,
			detail = f"post with id:{id} not found."
		)

	# update the post
	post_query.update(post.model_dump(), synchronize_session = False)

	# commit the changes to database
	db.commit()

	return post_query.first()
