from fastapi import APIRouter, status, HTTPException
from fastapi import Depends
# from typing import List, Optional
# import uuid

# Sqlalchemy imports
from app.database import get_db
from sqlalchemy.orm import Session
# from sqlalchemy import select

from app.model import models
from app.schema import schemas
from app.security import oauth

from app.logging.logger import logger

router = APIRouter(
	prefix="/course_votes",
	tags=['Course Votes']
)

@router.post("/", status_code = status.HTTP_201_CREATED)
async def vote(vote:schemas.Vote, db:Session = Depends(get_db), users_data:str = Depends(oauth.get_current_user)):
	# lets check if post exists
	post = db.query(models.PostJWT).filter(models.PostJWT.id == vote.post_id).first()
	if not post:
		logger.info(f"Post with id: {vote.post_id} does not exist")

		raise HTTPException(
			status_code = status.HTTP_404_NOT_FOUND,
			detail = f"Post with id: {vote.post_id} does not exist"
		)

	# query to find vote for given post and user
	vote_query = db.query(models.VoteJWT).filter(
			models.VoteJWT.post_id == vote.post_id,
			models.VoteJWT.user_id == users_data.id
		)

	# fetch existing vote
	found_vote = vote_query.first()

	# print(users_data.id)

	if (vote.dir == 1):
		# check if vote already exists
		if found_vote:
			logger.info(f"User {users_data.id} has already voted on post {vote.post_id}")

			raise HTTPException(
				status_code=status.HTTP_409_CONFLICT,
				detail=f"user {users_data.id} has already voted on post {vote.post_id}"
			)

		# create new vote
		new_vote = models.VoteJWT(post_id=vote.post_id, user_id=users_data.id)

		db.add(new_vote)
		db.commit()

		logger.info(f"User {users_data.id} voted on post {vote.post_id}")
		return {"message" : "successfully added vote"}

	else:
		# check if vote exists to delete
		if not found_vote:
			logger.info(f"Vote does not exist for user {users_data.id} on post {vote.post_id}")

			raise HTTPException(
				status_code = status.HTTP_404_NOT_FOUND,
				detail = "Vote does not exist"
			)

		# delete the vote
		vote_query.delete(synchronize_session=False)
		db.commit()

		logger.info(f"User {users_data.id} deleted vote on post {vote.post_id}")
		return {"message" : "successfully deleted vote"}
