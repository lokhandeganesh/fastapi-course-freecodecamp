from app.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import Base

# SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# or we can import database_url from settings
SQLALCHEMY_DATABASE_URL = settings.database_url + "_test"

engine = create_engine(
	SQLALCHEMY_DATABASE_URL
	# ,echo = True # enable logging of SQL queries
    )

with engine.begin() as conn:
	# conn.execute(text("CREATE SCHEMA IF NOT EXISTS course"))
	conn.execute(text("CREATE SCHEMA IF NOT EXISTS course_jwt"))


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

print("Database connection to Test databasewas succesfull!")

def override_get_db():
	db = TestingSessionLocal()
	try:
		yield db
	finally:
		db.close()