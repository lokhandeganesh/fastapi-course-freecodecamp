from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

import psycopg
from psycopg.rows import dict_row
import time

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(
	SQLALCHEMY_DATABASE_URL
	# ,echo = True # enable logging of SQL queries
    )

with engine.begin() as conn:
	conn.execute(text("CREATE SCHEMA IF NOT EXISTS course"))
	conn.execute(text("CREATE SCHEMA IF NOT EXISTS course_jwt"))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


# Database connection using psycopg

# conninfo string
conninfo = f"user={settings.database_username} password={settings.database_password} host={settings.database_hostname} port={settings.database_port} dbname={settings.database_name}"

# Attempt to connect to the database
while True:
    try:
        conn = psycopg.connect(conninfo = conninfo, row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)
