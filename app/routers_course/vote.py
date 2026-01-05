from fastapi import APIRouter, Response, status, HTTPException
from fastapi import Depends
from typing import List, Optional
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

@router.get("/")
async def vote():
    return {"message" : "This is the course vote router"}