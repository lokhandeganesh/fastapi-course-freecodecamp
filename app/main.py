from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.middleware.gzip import GZipMiddleware

# need to import models to create tables, moved to separate folder
# from .model import models

# from .database import engine

# from .config import settings

from fastapi_docshield import DocShield
from app.db_files.config import settings
# from app.db.db_config import settings

from app.logging.logger import logger

from contextlib import asynccontextmanager

from app.db_files.database import engine

from app.model.models import Base
from sqlalchemy import text

from app.db_files.redis import init_redis, close_redis

# routers for course
from app.routers import post, user, auth, vote
# from app.routers import drop_down_module

"""
uncomment me and related imports to create table in database,
only for first time, after that comment me to avoid dropping tables
"""
# models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Optional Redis
    try:
        await init_redis()
        logger.info("Redis connection established successfully.")
    except Exception as e:
        logger.warning(f"Optional Redis service is unavailable: {e}")

    # Database Schema & Table Initialization
    try:
        async with engine.begin() as conn:
            # Create the schema first
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS course"))

            # Create tables within that schema
            # run_sync bridges the gap between Async engine and Sync Base.metadata
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Database schema 'course' and tables verified/created.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # In production, you might want to raise this so the app doesn't start broken
        raise e

    yield  # The app runs here

    # Shutdown & Cleanup
    await close_redis()
    await engine.dispose()
    logger.info("Cleanup complete: Redis closed and DB engine disposed.")


app = FastAPI(
    lifespan=lifespan,
    root_path="/webservice",
    docs_url="/webservice/docs",
    redoc_url=None,
    openapi_url="/webservice/openapi.json",
    # makes curl show /webservice/...
    servers=[{"url": "/webservice"}],
    )

origins = ["*"]

# Add Gzip compression for any response larger than 1KB
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)
# External routers
# app.include_router(drop_down_module.router)


# Fetching user database for accessing docs

# Add protection to docs with multiple users
DocShield(
    app=app,
    credentials={
        "admin": settings.docshield_admin_pass,
        "developer": settings.docshield_developer_pass,
    }
)


@app.get("/")
def root():
    logger.info("Hi, Welcome to FastAPI application")
    return {"message": "Hello World pushing out to ubuntu"}


favicon_path = r"app/static/favicon.ico"  # Adjust path to file


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
