from sqlalchemy import create_engine, text
# from sqlalchemy.ext.declarative import declarative_base # old way deprecated
from sqlalchemy.orm import sessionmaker, declarative_base
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS course"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='password123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
