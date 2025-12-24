# from typing import Optional
from fastapi import APIRouter, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel

import uuid
from uuid import UUID

from random import randrange
from app.logger import logger

# Sqlalchemy imports
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app import models

# psycopg imports
from app.database import conn, cursor

router = APIRouter(
	prefix="/course",
	tags=['Course']
)

# function to validate Uuid
def is_valid_uuid(uuid_to_test, version=4):
    try:
        # check for validity of Uuid
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return True

# /course/
# /Course

# Root router
@router.get('/')
async def get_root():
	return {"message" : "Hello World"}

# # get method to retrive posts
# @router.get("/posts")
# async def get_posts():
# 	return {"data" : "This is your posts"}


# # post method to create post
# @router.post("/create_posts")
# async def create_posts(payload: dict = Body(...)):
# 	# print(payload)
# 	return {"new_post" : f"title {payload['title']}"}


class Post(BaseModel):
	title: str
	content: str
	published: bool = True
	owner_id : int

# @router.post("/create_posts_model")
# async def create_posts_model(post: Post):
# 	# to access parameters as dict use .model_dump()
# 	print(post.model_dump())
# 	return {
# 		"data" : f"title {post.title}",
# 		"post" : post
# 		}

# CRUD Operations
my_posts = [
	{
		"id": 1 , "title" : "title of post 1",
		"content" : "content of post 1",
		"published": True
	},
	{
		"id": 2 , "title" : "title of post 2",
		"content" : "content of post 2",
		"published": True
	}
]

def find_post(id):
	for p in my_posts:
		if (p["id"] == id):
			return p

def find_index_post(id):
	for i, p in enumerate(my_posts):
		if (p["id"] == id) :
			return i

@router.get("/posts")
async def get_posts():
	return {"data" : my_posts}

# post method to create post
@router.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_posts(post:Post):
	post_dict = post.model_dump()
	post_dict['id'] = randrange(0, 1000000000)
	my_posts.append(post_dict)

	# print(post_dict)
	return {"data" : my_posts}

# to retrive latest post from posts
@router.get("/posts/latest")
async def get_latest_post():
	post = my_posts[len(my_posts) - 1]
	return {"data" : post}

# to retrive post from posts
@router.get("/posts/{id}")
async def get_post(id:int, response: Response):
	try:
		post  = find_post(id)

		if not post:
			logger.info(f"post with id:{id} not found.")

			# response.status_code = status.HTTP_404_NOT_FOUND
			# return {"message" : f"post with id:{id} not found."}

			raise HTTPException(
				status_code = status.HTTP_404_NOT_FOUND,
				detail = f"post with id:{id} not found."
				)
		return {"data" : post}
	except HTTPException:
		# Let FastAPI handle HTTPException (like 404)
		raise
	except Exception as e:
		# Log the exception for debugging
		logger.exception(f"Unhandled error: {e}")

# to retrive item by uuid
@router.get("/items/{id}")
async def get_post_by_uuid(id:UUID, response: Response):
	try:
		# Code logic here

		return {"data" : id}
	except HTTPException:
		# Let FastAPI handle HTTPException (like 404)
		raise
	except Exception as e:
		# Log the exception for debugging
		logger.exception(f"Unhandled error: {e}")

@router.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
	# using index of in posts
	index = find_index_post(id)

	if not index:
		raise HTTPException(
			status_code= status.HTTP_404_NOT_FOUND,
			detail = f"post with id:{id} not found."
		)

	my_posts.pop(index)
	return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}")
async def update_post(id:int, post:Post):
	# using index of in posts
	index = find_index_post(id)

	if not index:
		raise HTTPException(
			status_code= status.HTTP_404_NOT_FOUND,
			detail = f"post with id:{id} not found."
		)

	post_dict = post.model_dump()
	post_dict["id"] = id
	my_posts[index] = post_dict

	return {"data" : post_dict}


# Working with database
"""Database is a collectio of organized data that can be easily accessed and managed"""
@router.get("/db_posts")
async def get_db_posts():
	cursor.execute("SELECT * FROM course.posts")
	posts = cursor.fetchall()
	return {"data" : posts}

# post method to create course.post
@router.post("/db_posts", status_code = status.HTTP_201_CREATED)
async def create_db_posts(post:Post):
	cursor.execute(
		"""INSERT INTO course.posts (title, content, published, owner_id)
		VALUES (%s, %s, %s, %s) RETURNING *""",
		(post.title, post.content, post.published, post.owner_id))

	new_post = cursor.fetchone()
	conn.commit()
	# print(post_dict)
	return {"data" : new_post}

# to retrive post from posts
@router.get("/db_posts/{id}")
async def get_db_post(id:int, response: Response):
	cursor.execute("""SELECT * FROM course.posts WHERE id = %s""",	(str(id),))
	post = cursor.fetchone()

	try:
		if not post:
			logger.info(f"post with id:{id} not found.")

			raise HTTPException(
				status_code = status.HTTP_404_NOT_FOUND,
				detail = f"post with id:{id} not found."
				)
		return {"data" : post}
	except HTTPException:
		# Let FastAPI handle HTTPException (like 404)
		raise
	except Exception as e:
		# Log the exception for debugging
		logger.exception(f"Unhandled error: {e}")

@router.delete("/db_posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_db_post(id:int):
	cursor.execute("""DELETE FROM course.posts WHERE id = %s RETURNING *""", (str(id),))
	deleted_post = cursor.fetchone()

	conn.commit()

	if not deleted_post:
		raise HTTPException(
			status_code= status.HTTP_404_NOT_FOUND,
			detail = f"post with id:{id} not found."
		)

	return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/db_posts/{id}")
async def update_db_post(id:int, post:Post):
	cursor.execute(
		"""
		UPDATE course.posts
			SET
				title = %s, content = %s,
				published = %s, owner_id = %s
		WHERE id = %s RETURNING *""", (
			post.title, post.content,
			post.published, post.owner_id,
			str(id),))

	updated_post = cursor.fetchone()

	conn.commit()

	# using index of in posts
	if not updated_post:
		raise HTTPException(
			status_code= status.HTTP_404_NOT_FOUND,
			detail = f"post with id:{id} not found."
		)

	return {"data" : updated_post}

# Connections from sqlalchemy
@router.get("/sqla_posts")
async def get_sqla_posts(db:Session = Depends(get_db)):
	posts = db.query(models.Post).all()
	return {"data" : posts}

# post method to create course.post
@router.post("/sqla_posts", status_code = status.HTTP_201_CREATED)
async def create_sqla_posts(post:Post, db:Session = Depends(get_db)):
	# print(post.model_dump())
	new_post = models.Post(**post.model_dump())

	# add new_post to session
	db.add(new_post)
	# commit the changes to database
	db.commit()
	# refresh the new_post object to get updated data from database
	db.refresh(new_post)

	return {"data" : new_post}

# to retrive post from posts
@router.get("/sqla_posts/{id}")
async def get_sqla_post(id:int, response: Response, db:Session = Depends(get_db)):

	# query to get post by id
	post = db.query(models.Post).filter(models.Post.id == id).first()

	try:
		if not post:
			logger.info(f"post with id:{id} not found.")

			raise HTTPException(
				status_code = status.HTTP_404_NOT_FOUND,
				detail = f"post with id:{id} not found."
				)
		return {"data" : post}
	except HTTPException:
		# Let FastAPI handle HTTPException (like 404)
		raise
	except Exception as e:
		# Log the exception for debugging
		logger.exception(f"Unhandled error: {e}")

# to delete post from course.posts table
@router.delete("/sqla_posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_sqla_post(id:int, db:Session = Depends(get_db)):

	# query to delete post by id
	post = db.query(models.Post).filter(models.Post.id == id)

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
@router.put("/sqla_posts/{id}")
async def update_sqla_post(id:int, post:Post, db:Session = Depends(get_db)):

	# query to update post by id
	post_query = db.query(models.Post).filter(models.Post.id == id)

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

	return {"data" : post_query.first()}
