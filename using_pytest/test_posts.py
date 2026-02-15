import pytest
from app.schema import schemas

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/course_posts/")
    # print(response.json())

    posts = [schemas.PostRetrieveBase(**post) for post in response.json()]
    # print(posts)

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/course_posts/")
    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/course_posts/9999/")

    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/course_posts/{test_posts[0].id}/")
    print(response.json())

    post = schemas.PostRetrieveBase(**response.json())

    assert response.status_code == 200
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize(
    "title, content, published",
    [
    ("new awesome title", "new awesome content", True),
    ("food title", "food content", True),
    ("travel title", "travel content", True),
    ])
def test_create_post(authorized_client, test_create_user, test_posts, title, content, published):
    response = authorized_client.post(
        url = "/course_posts/",
        json = {
            "title" : title,
            "content" : content,
            "published" : published,
            "owner_id" : test_create_user["id"]
        }
    )

    created_post = schemas.PostCreate(**response.json())
    assert response.status_code == 201
    assert created_post.title == title

def test_unauthorized_create_post(client, test_create_user, test_posts):
    response = client.post(
        url = "/course_posts/",
        json = {
            "title" : "title for unauthorized user",
            "content" : "content for unauthorized user",
            "published" : True,
            "owner_id" : test_create_user["id"]
        }
    )

    assert response.status_code == 401

def test_unauthorized_delete_post(client, test_create_user, test_posts):
    response = client.delete(
        url = f"/course_posts/{test_posts[0].id}")

    assert response.status_code == 401

def test_delete_post(authorized_client, test_create_user, test_posts):
    response = authorized_client.delete(
        url = f"/course_posts/{test_posts[0].id}")

    assert response.status_code == 204

def test_delete_post_not_exist(authorized_client, test_create_user, test_posts):
    response = authorized_client.delete(
        url = "/course_posts/9999")

    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_create_user, test_posts):
    response = authorized_client.delete(
        url = f"/course_posts/{test_posts[3].id}")

    assert response.status_code == 403

def test_update_post(authorized_client, test_create_user, test_posts):
    data = {
        "title" : "updated title",
        "content" : "updated content",
        "published" : False,
        "owner_id" : test_create_user["id"]
    }
    response = authorized_client.put(
        url = f"/course_posts/{test_posts[0].id}",
        json = data
    )

    assert response.status_code == 200

def test_update_other_post(authorized_client, test_create_user2, test_posts):
    data = {
        "title" : "other updated title",
        "content" : "other updated content",
        "published" : False,
        "owner_id" : test_create_user2["id"]
    }
    response = authorized_client.put(
        url = f"/course_posts/{test_posts[3].id}",
        json = data
    )

    assert response.status_code == 403

def test_unauthorized_update_post(client, test_create_user, test_posts):
    data = {
        "title" : "other updated title",
        "content" : "other updated content",
        "published" : False,
        "owner_id" : test_create_user["id"]
    }
    response = client.put(
        url = f"/course_posts/{test_posts[3].id}",
        json = data
    )

    assert response.status_code == 401

def test_update_post_not_exist(authorized_client, test_create_user, test_posts):
    data = {
        "title" : "other updated title",
        "content" : "other updated content",
        "published" : False,
        "owner_id" : test_create_user["id"]
    }

    response = authorized_client.put(
        url = "/course_posts/9999",
        json = data)

    assert response.status_code == 404
