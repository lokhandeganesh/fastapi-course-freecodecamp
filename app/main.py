from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# from . import models
# from .database import engine
# from .config import settings
from .routers import post, user, auth, vote, course_pract


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course_pract.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}

favicon_path = "favicon.ico"  # Adjust path to file
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
	return FileResponse(favicon_path)
