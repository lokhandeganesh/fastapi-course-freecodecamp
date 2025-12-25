from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class PostJWT(Base):
	__table_args__ = {"schema": "course_jwt"}
	__tablename__ = "posts"

	id = Column(Integer, primary_key=True, nullable=False)
	title = Column(String, nullable=False)
	content = Column(String, nullable=False)
	published = Column(Boolean, server_default='TRUE', nullable=False)
	created_at = Column(
		TIMESTAMP(timezone=True),
		nullable=False,
		server_default=text('now()')
		)
	owner_id = Column(
		Integer,
		ForeignKey(
			"course_jwt.users.id",
			ondelete="CASCADE"),
		nullable=False
		)

	owner = relationship("UserJWT")


class UserJWT(Base):
	__table_args__ = {"schema": "course_jwt"}
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, nullable=False)
	email = Column(String, nullable=False, unique=True)
	password = Column(String, nullable=False)
	created_at = Column(
		TIMESTAMP(timezone=True),
		nullable=False,
		server_default=text('now()')
		)


class VoteJWT(Base):
	__table_args__ = {"schema": "course_jwt"}
	__tablename__ = "votes"

	user_id = Column(
		Integer,
		ForeignKey(
			"course_jwt.users.id",
			ondelete="CASCADE"),
		primary_key=True
		)
	post_id = Column(
		Integer,
		ForeignKey(
			"course_jwt.posts.id",
			ondelete="CASCADE"),
		primary_key=True
		)
