from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# All functionalities of response object can be used here
# please refer official documentation of response library for more details

def test_root():
    response  = client.get("/")
    # print(response.json())
    assert response.status_code == 200

def test_create_user():
    response = client.post(
        "/course_users/",
        json={"email": "test@example.com", "password": "testpassword"}
        )
    print(response.json())
    assert response.status_code == 201