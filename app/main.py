from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# from . import models

# need to import models to create tables, moved to separate folder
# from .model import models

# from .database import engine

# from .config import settings

from .routers import post, user, auth, vote, course_pract
# routers for course
from .routers_course import post as course_post, user as course_user, auth as course_auth, vote as course_vote

from fastapi_docshield import DocShield
from .config import settings
# from app.db.db_config import settings
from app.logging.logger import logger


# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
	# lifespan=lifespan,
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

app.include_router(course_pract.router)

app.include_router(course_post.router)
app.include_router(course_user.router)
app.include_router(course_vote.router)
app.include_router(course_auth.router)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Fetching user database for accessing docs

# Add protection to docs with multiple users
DocShield(
	app=app,
	credentials={
		"admin": settings.docshield_admin_pass,
		"developer":settings.docshield_developer_pass,
	}
)

@app.get("/")
def root():
	logger.info("Hi, Welcome to FastAPI application")
	return {"message": "Hello World pushing out to ubuntu with live changes!"}

favicon_path = r"app/static/favicon.ico"  # Adjust path to file
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
	return FileResponse(favicon_path)
