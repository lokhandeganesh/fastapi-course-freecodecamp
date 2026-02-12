from fastapi.testclient import TestClient
from app.main import app
from app.schema import schemas
from app.database import get_db
from using_pytest.database_test import override_get_db

# Lets override our get_db dependency to use the testing database instead of the
# production database for testing purposes.
app.dependency_overrides[get_db] = override_get_db

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

    # print(response.json())
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "test@example.com"
    assert response.status_code == 201