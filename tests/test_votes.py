import pytest
from app.model import models


@pytest.fixture()
def test_vote(test_posts, session, test_create_user):
    new_vote = models.VoteJWT(
        post_id=test_posts[3].id,
        user_id=test_create_user['id']
        )

    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    data = {
        "post_id": test_posts[0].id,
        "dir": 1
    }

    response = authorized_client.post(
        url="/course_votes/",
        json=data)

    assert response.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    data = {
        "post_id": test_posts[3].id,
        "dir": 1
    }

    response = authorized_client.post(
        url="/course_votes/",
        json=data)

    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    data = {
        "post_id": test_posts[3].id,
        "dir": 0
    }

    response = authorized_client.post(
        url="/course_votes/",
        json=data)

    assert response.status_code == 201


def test_delete_vote_non_exits(authorized_client, test_posts):
    data = {
        "post_id": test_posts[3].id,
        "dir": 0
    }

    response = authorized_client.post(
        url="/course_votes/",
        json=data)

    assert response.status_code == 404


def test_vote_post_non_exits(authorized_client, test_posts):
    data = {
        "post_id": 99,
        "dir": 1
    }

    response = authorized_client.post(
        url="/course_votes/",
        json=data)

    assert response.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    data = {
        "post_id": test_posts[3].id,
        "dir": 1
    }

    response = client.post(
        url="/course_votes/",
        json=data)

    assert response.status_code == 401
