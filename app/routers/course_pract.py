from typing import Optional
from fastapi import APIRouter
from fastapi.params import Body
from pydantic import BaseModel


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

# get method to retrive posts
@router.get("/posts")
async def get_posts():
	return {"data" : "This is your posts"}


# post method to create post
@router.post("/create_posts")
async def create_posts(payload: dict = Body(...)):
	# print(payload)
	return {"new_post" : f"title {payload['title']}"}


class Post(BaseModel):
	title: str
	content: str
	published: bool = True
	rating : Optional[int] = None

@router.post("/create_posts_model")
async def create_posts_model(payload: Post):
	# print(payload)
	return {
		"data" : f"title {payload.title}"
		}
