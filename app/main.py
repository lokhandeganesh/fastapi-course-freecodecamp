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

import asyncpg
from contextlib import asynccontextmanager

"""
uncomment me and related imports to create table in database,
only for first time, after that comment me to avoid dropping tables
"""
# models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # app.redis = await get_redis()
    postgres_dsn = settings.postgres_url.unicode_string()
    try:
        app.postgres_pool = await asyncpg.create_pool(
            dsn=postgres_dsn,
            min_size=5,
            max_size=20,
        )
        logger.info(
            "Postgres pool created", idle_size=app.postgres_pool.get_idle_size()
        )
        yield
    except Exception as e:
        logger.error("Error during app startup", error=repr(e))
        raise
    finally:
        # await app.redis.close()
        await app.postgres_pool.close()


def create_app() -> FastAPI:
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

    return app


app = create_app()
