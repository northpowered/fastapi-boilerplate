from fastapi.testclient import TestClient
from app import create_app
from .payloads import test_superuser_1, test_user_1
from .shared import prepare_db_with_users

app = create_app()
client = TestClient(app)
api_version: str = 'v1'
application_name: str = 'accounting'
base_url: str = f"/{api_version}/{application_name}/"


def authenticate_as(user) -> str:
    response = client.post(
        "/auth/token",
        data={
            'username': user.username,
            'password': user.password
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    assert response.status_code == 200
    auth_data: dict = response.json()
    return f"{auth_data.get('token_type')} {auth_data.get('access_token')}"


def test_auth_as_superuser():
    prepare_db_with_users(test_superuser_1, test_user_1)
    response = authenticate_as(test_superuser_1)
    assert isinstance(response, str)


def test_user_get_all_unauth():
    response = client.get("/v1/accounting/users/")
    assert response.status_code == 401


def test_user_get_all():
    prepare_db_with_users(test_superuser_1, test_user_1)
    response = client.get(
        f"{base_url}users",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


