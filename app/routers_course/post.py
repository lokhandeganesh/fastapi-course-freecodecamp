from fastapi import APIRouter, Response, status, HTTPException
from fastapi import Depends
from typing import List, Optional
# import uuid

# Sqlalchemy imports
from app.database import get_db
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func #, select

from app.model import models
from app.schema import schemas
from app.security import oauth

from app.logging.logger import logger

router = APIRouter(
	prefix="/course_posts",
	tags=['Course Posts']
)

# Connections from sqlalchemy
@router.get("/", response_model = List[schemas.PostRetrieveOut])
async def get_course_posts(db:Session = Depends(get_db), limit:int = 5, skip:int = 0, search:Optional[str] = ""):
	# checking path parameter
	# print(limit)

	# query to get all posts
	# posts = db.query(models.PostJWT).all()

	# limiting number of posts returned
	# posts = db.query(models.PostJWT).filter(
	# 			models.PostJWT.title.contains(search)
	# 		).order_by(
	# 				models.PostJWT.id
	# 			).limit(limit).offset(skip).all()

	# to load only specific columns
	# stmt = select(
	# 	models.PostJWT.id,
	# 	models.PostJWT.title,
	# 	models.PostJWT.content,
	# 	models.PostJWT.published,
	# 	models.PostJWT.owner_id
	# 	)

	# posts = db.execute(stmt).mappings().all()

	# performing joins of posts and votes
	# We need to use aliasing because ORM and Pydantic have trouble
	# handling models with the schema output name conflicts
	PostAlias = aliased(models.PostJWT, name="Post")

	posts = db.query(
		PostAlias,
		func.count(models.VoteJWT.post_id).label("votes")
		).join(
			models.VoteJWT,
			models.VoteJWT.post_id == PostAlias.id,
			isouter=True
			).group_by(
				PostAlias.id
				).filter(
					PostAlias.title.contains(search)
					).limit(limit).offset(skip).all()

	# return [{"Post": post, "votes": votes} for post, votes in posts]
	return posts

# post method to create course.post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostRetrieve)
async def create_course_posts(
	post:schemas.PostBase, db:Session = Depends(get_db),
	users_data = Depends(oauth.get_current_user)):

	# we can access user data from token_data
	# print(users_data.id)

	# print(post.model_dump())
	new_post = models.PostJWT(
		**post.model_dump(),
		owner_id = users_data.id)

	# add new_post to session
	db.add(new_post)
	# commit the changes to database
	db.commit()
	# refresh the new_post object to get updated data from database
	db.refresh(new_post)

	return new_post

# to retrive post from posts
@router.get("/{id}", response_model = schemas.PostRetrieveOut)
async def get_course_post(
	id:int, response: Response, db:Session = Depends(get_db),
	users_data:str = Depends(oauth.get_current_user)
	):

	# we can access user data from token_data
	# print(users_data.id)

	# query to get post by id
	PostAlias = aliased(models.PostJWT, name="Post")
	# post = db.query(models.PostJWT).filter(models.PostJWT.id == id).first()

	post = db.query(
			PostAlias,
			func.count(models.VoteJWT.post_id).label("votes")
			).join(
				models.VoteJWT,
				models.VoteJWT.post_id == PostAlias.id,
				isouter=True
				).filter(
					PostAlias.id == id
					).group_by(
						PostAlias.id
						).first()

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
async def delete_course_post(
	id:int, db:Session = Depends(get_db),
	users_data:str = Depends(oauth.get_current_user)):

	# we can access user data from token_data
	# print(users_data.id)

	# query to delete post by id
	post_query = db.query(models.PostJWT).filter(models.PostJWT.id == id)

	# retrive the post for deleting
	post = post_query.first()

	if not post:
		logger.info(f"post with id:{id} not found.")

		raise HTTPException(
			status_code= status.HTTP_404_NOT_FOUND,
			detail = f"post with id:{id} not found."
		)

	# we will chekk if the user is the owner of the post before deleting
	if not post.owner_id == users_data.id:
		logger.info(f"user is not owner of post with id:{id}.")
		raise HTTPException(
			status_code= status.HTTP_403_FORBIDDEN,
			detail = "Not authorized to perform requested action."
		)

	# delete the post
	post_query.delete(synchronize_session=False)

	# commit the changes to database
	db.commit()

	logger.info(f"post with id:{id} deleted.")

	return Response(status_code=status.HTTP_204_NO_CONTENT)

# to update post from course.posts table
@router.put("/{id}")
async def update_course_post(
	id:int, post:schemas.PostCreate, db:Session = Depends(get_db),
	users_data:str = Depends(oauth.get_current_user)):

	# we can access user data from token_data
	# print(users_data.id)

	# query to update post by id
	post_query = db.query(models.PostJWT).filter(models.PostJWT.id == id)

	# retrive the post for updating
	updated_post = post_query.first()

	# using index of in posts
	if not updated_post:
		logger.info(f"post with id:{id} not found.")
		raise HTTPException(
			status_code= status.HTTP_404_NOT_FOUND,
			detail = f"post with id:{id} not found."
		)

	# we will chekk if the user is the owner of the post before updating
	if not updated_post.owner_id == users_data.id:
		logger.info(f"user is not owner of post with id:{id}.")
		raise HTTPException(
			status_code= status.HTTP_403_FORBIDDEN,
			detail = "Not authorized to perform requested action."
		)

	# update the post
	post_query.update(post.model_dump(), synchronize_session = False)

	# commit the changes to database
	db.commit()

	logger.info(f"post with id:{id} updated.")

	return post_query.first()
