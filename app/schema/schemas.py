from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
import uuid



class PostBase(BaseModel):
	title: str
	content: str
	published: bool = True

class PostCreateUp(PostBase):
	# owner_id: uuid.UUID
	id: int

	class Config:
		# this method is deprecated in Pydantic v2
		# orm_mode = True
		from_attributes = True

class PostRetrieve(PostBase):
	id: int
	owner_id: uuid.UUID

	class Config:
		# this method is deprecated in Pydantic v2
		# orm_mode = True
		from_attributes = True

class PostCreation(PostBase):
	owner_id: uuid.UUID

	class Config:
		# this method is deprecated in Pydantic v2
		# orm_mode = True
		from_attributes = True


class PostCreate(PostBase):
	pass


class UserOut(BaseModel):
	id: uuid.UUID
	email: EmailStr
	created_at: datetime

	class Config:
		from_attributes = True


class Post(PostBase):
	id: int
	created_at: datetime
	owner_id: int
	owner: UserOut

	class Config:
		from_attributes = True


class PostOut(BaseModel):
	Post: Post
	votes: int

	class Config:
		from_attributes = True


class UserCreate(BaseModel):
	email: EmailStr
	password: str


class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	id: Optional[uuid.UUID] = None


class Vote(BaseModel):
	post_id: int
	dir: int = Field(..., le=1)
