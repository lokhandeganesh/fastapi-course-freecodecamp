from typing import Optional
from fastapi import APIRouter
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange

router = APIRouter(
	prefix="/course",
	tags=['Course']
)

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
	rating : Optional[int] = 1

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
		"published": True,
		"rating": 4
	},
	{
		"id": 2 , "title" : "title of post 2",
		"content" : "content of post 2",
		"published": True,
		"rating": 4
	}
]

@router.get("/posts")
async def get_posts():
	return {"data" : my_posts}

# post method to create post
@router.post("/posts")
async def create_posts(post: Post):
	post_dict = post.model_dump()
	post_dict['id'] = randrange(0, 1000000000)
	my_posts.append(post_dict)

	# print(post_dict)
	return {"data" : my_posts}