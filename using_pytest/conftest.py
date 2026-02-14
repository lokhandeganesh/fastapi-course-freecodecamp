from .databasetest import session, client
import pytest
"""
    Share Fixtures -
    Any fixtures defined in conftest.py are available
    to all test
    files in that directory and any subdirectories.
"""
__all__ = ["session", "client"]


@pytest.fixture
def test_create_user(client):
    user_data = {
            "email": "test@example.com",
            "password": "testpassword"
            }

    response = client.post(
        url = "/course_users/",
        json = user_data)

    # new_user = schemas.UserOut(**response.json())
    new_user = response.json()
    print(new_user)

    new_user["password"] = user_data["password"]

    assert new_user["email"] == "test@example.com"
    assert response.status_code == 201
    return new_user