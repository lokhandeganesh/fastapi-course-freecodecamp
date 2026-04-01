from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# need to import models to create tables, moved to separate folder
# from .model import models

# from .database import engine

# from .config import settings

# routers for course
from app.routers import post, user, auth, vote

from fastapi_docshield import DocShield
from app.db_files.config import settings
# from app.db.db_config import settings

from app.logging.logger import logger

from contextlib import asynccontextmanager
# from sqlalchemy import text

from app.db_files.database import engine
# from app.model.models import Base

"""
uncomment me and related imports to create table in database,
only for first time, after that comment me to avoid dropping tables
"""
# models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # RUNS ONCE ON STARTUP
    # async with engine.begin() as conn:
    #     # Create the schema
    #     await conn.execute(text("CREATE SCHEMA IF NOT EXISTS course"))

    #     # Create the tables (Async version of create_all)
    #     await conn.run_sync(Base.metadata.create_all)

    # logger.info("Schema 'course' and tables verified/created.")

    yield  # The app runs here

    # RUNS ONCE ON SHUTDOWN
    await engine.dispose()
    logger.info("Database engine disposed.")

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
