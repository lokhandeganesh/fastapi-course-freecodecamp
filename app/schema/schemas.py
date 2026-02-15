from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
import uuid
from datetime import datetime as dt

current_datetime_local = dt.now().isoformat()

class UserOut(BaseModel):
	id: uuid.UUID
	email: EmailStr
	# created_at: datetime = current_datetime_local

	class Config:
		from_attributes = True

class PostBase(BaseModel):
	title: str
	content: str
	published: bool = True
	created_at: Optional[datetime] = current_datetime_local

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

class PostRetrieveOwner(PostBase):
	id: int
	# owner_id: uuid.UUID

	# defining owner as UserOut schema
	owner: UserOut

	class Config:
		# this method is deprecated in Pydantic v2
		# orm_mode = True
		from_attributes = True

class PostRetrieveOut(BaseModel):
	Post: PostRetrieveOwner
	votes: int

	class Config:
		from_attributes = True

class PostRetrieveBase(BaseModel):
	Post: PostBase
	votes: int

	class Config:
		from_attributes = True

class PostCreation(PostBase):
	owner_id: uuid.UUID

	class Config:
		# this method is deprecated in Pydantic v2
		# orm_mode = True
		from_attributes = True


class PostCreate(PostBase):
	pass



class Post(PostBase):
	id: int
	created_at: datetime = current_datetime_local
	owner_id: uuid.UUID
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
	phone_number: Optional[str] = None
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
