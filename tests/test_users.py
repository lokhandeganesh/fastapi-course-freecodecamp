import pytest
import jwt
import uuid

# from fastapi.testclient import TestClient
# from app.main import app
from app.schema import schemas
# from app.database import get_db
# from using_pytest.database_test import override_get_db

# from .databasetest import client, session

# Lets override our get_db dependency to use the testing database instead of the
# production database for testing purposes.
# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

# All functionalities of response object can be used here
# please refer official documentation of response library for more details

# from using_pytest.databasetest import client, session
from app.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

"""
Automatic Fixture Discovery -
    Pytest automatically finds and loads conftest.py in
    your test directories
conftest.py
"""


def test_root(client):
    response = client.get(url="/")
    # print(response.json())
    assert response.status_code == 200


"""
    # def test_create_user(client):
    #     response = client.post(
    #         url = "/course_users/",
    #         json = {
    #             "email": "test@example.com",
    #             "password": "testpassword"
    #             })

    #     # print(response.json())
    #     new_user = schemas.UserOut(**response.json())
    #     assert new_user.email == "test@example.com"
    #     assert response.status_code == 201

    # def test_login_user(client):
    #     response = client.post(
    #         url = "/course_auth/login/",
    #         data = {
    #             "username": "test@example.com",
    #             "password": "testpassword"
    #             })

    #     # print(response.json())
    #     assert response.status_code == 200
"""


@pytest.fixture
def test_create_user(client):
    user_data = {
            "email": "test@example.com",
            "password": "testpassword"
            }

    response = client.post(
        url="/course_users/",
        json=user_data)

    # new_user = schemas.UserOut(**response.json())
    new_user = response.json()
    # print(new_user)

    new_user["password"] = user_data["password"]

    assert new_user["email"] == "test@example.com"
    assert response.status_code == 201
    return new_user


def test_login_user(client, test_create_user):
    user_data = {
            "username": test_create_user["email"],
            "password": test_create_user["password"]
            }

    response = client.post(
        url="/course_auth/login/",
        data=user_data
        )

    login_res = schemas.Token(**response.json())
    # print(login_res)

    # Decode the JWT token
    payload = jwt.decode(
        jwt=login_res.access_token,
        key=SECRET_KEY,
        algorithms=[ALGORITHM])

    # Extract the user_id from the payload
    user_id: uuid.UUID = payload.get("sub")
    assert user_id == test_create_user["id"]
    assert login_res.token_type == "bearer"

    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@example.com", "Password", 403),
        ("test@example.com", "wrongPassword", 403),
        ("test@example.com", None, 403),
        ("wrong@example.com", "wrongPassword", 401),
        (None, "wrongPassword", 401)
    ]
)
def test_incorrect_login(client, test_create_user, email, password, status_code):
    user_data = {
            "username": email,
            "password": password
        }

    response = client.post(
        url="/course_auth/login/",
        data=user_data
        )

    assert response.status_code == status_code
    # assert response.json()["detail"] == "Invalid Credentials"
