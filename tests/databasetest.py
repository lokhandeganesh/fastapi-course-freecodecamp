from fastapi.testclient import TestClient
from app.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker  # , declarative_base

from app.main import app
from app.database import Base
from app.database import get_db

import pytest

# SQLALCHEMY_DATABASE_URL= f'postgresql+psycopg://\
#     {settings.database_username}:\
#     {settings.database_password}@{settings.database_hostname}:\
#         {settings.database_port}/{settings.database_name}_test'

# or we can import database_url from settings
SQLALCHEMY_DATABASE_URL = settings.database_url + "_test"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # ,echo = True # enable logging of SQL queries
    )

with engine.begin() as conn:
    # conn.execute(text("CREATE SCHEMA IF NOT EXISTS course"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS course_jwt"))


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

"""
The scope of the fixture is depending on how many times you want to run
the setup and teardwon code, the default one is "function", if you want to
    run it once
        * per test function then use scope="function",
        * per test class then use scope="class",
        * per test module then use scope="module",
        * per test session then use scope="session"
"""


# @pytest.fixture(scope="module")
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database connection to Test database was succesfull!")
    db = TestingSessionLocal()
    # run our code before we run our tests
    try:
        yield db
    finally:
        db.close()


# @pytest.fixture(scope="module")
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
