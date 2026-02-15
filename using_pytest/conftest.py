from .databasetest import session, client
import pytest
from app.security import oauth2
from app.model import models

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
    # print(new_user)

    new_user["password"] = user_data["password"]

    assert new_user["email"] == "test@example.com"
    assert response.status_code == 201
    return new_user

@pytest.fixture
def test_create_user2(client):
    user_data = {
            "email": "test2@example.com",
            "password": "test2password"
            }

    response = client.post(
        url = "/course_users/",
        json = user_data)

    # new_user = schemas.UserOut(**response.json())
    new_user = response.json()
    # print(new_user)

    new_user["password"] = user_data["password"]

    assert new_user["email"] == "test2@example.com"
    assert response.status_code == 201
    return new_user

@pytest.fixture
def token(test_create_user):
    access_token = oauth2.create_access_token(
        data = {
            "id" : test_create_user["id"]
            }
    )

    # print(access_token)
    return access_token

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(session, test_create_user, test_create_user2):
    posts_data = [
        {
            "title" : "first title",
            "content" : "first content",
            "owner_id" : test_create_user["id"]
        },
        {
            "title" : "second title",
            "content" : "second content",
            "owner_id" : test_create_user2["id"]
        }
    ]

    def create_post_model(post):
        return models.PostJWT(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)

    session.add_all(posts)
    # # or you can pass list of posts to add_all method like session.add_all([post1, post2])
    # session.add_all(
    #     [
    #         models.PostJWT( posts_data[0]["title"], posts_data[0]["content"], posts_data[0]["owner_id"]),
    #         models.PostJWT( posts_data[1]["title"], posts_data[1]["content"], posts_data[1]["owner_id"]),
    #     ]
    # )

    session.commit()

    posts = session.query(models.PostJWT).all()
    # print(posts)
    return posts
