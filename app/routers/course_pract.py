from typing import Optional
from fastapi import APIRouter, Response, status, HTTPException
# from fastapi.params import Body
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
	post  = find_post(id)

	if not post:
		# response.status_code = status.HTTP_404_NOT_FOUND
		# return {"message" : f"post with id:{id} not found."}

		raise HTTPException(
			status_code = status.HTTP_404_NOT_FOUND,
			detail = f"post with id:{id} not found."
			)
	return {"data" : post}

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
