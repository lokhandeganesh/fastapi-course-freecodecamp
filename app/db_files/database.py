from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.db_files.config import settings

# or we can import database_url from settings
SQLALCHEMY_DATABASE_URL = settings.database_url
# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # ,echo = True # enable logging of SQL queries
    )

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS course"))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

print("Database connection was succesfull!")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
