import json
from fastapi.testclient import TestClient
from app import create_app
from .payloads import (
    test_superuser_1,
    test_user_1,
    test_user_2,
    test_role_1,
    test_group_1,
)
from .payload_models import UserModel
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


def test_create_user():
    prepare_db_with_users(test_superuser_1, test_user_1)
    response = client.post(
        f"{base_url}users/",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        },
        data=test_user_2.json()
    )
    assert response.status_code == 201
    assert response.json().get('id')
    return response.json().get('id')


def test_get_user_by_id():
    prepare_db_with_users(test_superuser_1, test_user_1)
    user_id: str = test_create_user()
    response = client.get(
        f"{base_url}users/{user_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 200
    assert response.json().get('id') == user_id
    assert response.json().get('username') == test_user_2.username


def test_update_user_by_id():
    prepare_db_with_users(test_superuser_1, test_user_1)
    user_id: str = test_create_user()
    response = client.put(
        f"{base_url}users/{user_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1),
                'Content-Type': 'application/json'
        },
        json={'username': 'new_username'}
    )
    assert response.status_code == 200
    assert response.json().get('id') == user_id
    assert response.json().get('username') != test_user_2.username
    assert response.json().get('username') == 'new_username'


def test_change_user_password():
    prepare_db_with_users(test_superuser_1, test_user_1)
    user_id: str = test_create_user()
    assert authenticate_as(test_user_2)
    response = client.patch(
        f"{base_url}users/{user_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1),
                'Content-Type': 'application/json'
        },
        json={
            'old_password': test_user_2.password,
            'new_password': 'new_password'
        }
    )
    assert response.status_code == 200
    assert authenticate_as(
        UserModel(
            username=test_user_2.username,
            password='new_password',
            email='foobar@mail.com'
        )
    )


def test_delete_user():
    prepare_db_with_users(test_superuser_1, test_user_1)
    user_id: str = test_create_user()
    response = client.delete(
        f"{base_url}users/{user_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 204
    response = client.get(
        f"{base_url}users/{user_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 404


def test_create_role():
    prepare_db_with_users(test_superuser_1, test_user_1)
    response = client.post(
        f"{base_url}roles/",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        },
        data=test_role_1.json()
    )
    assert response.status_code == 201
    assert response.json().get('id')
    return response.json().get('id')


def test_get_all_roles():
    test_create_role()
    response = client.get(
        f"{base_url}roles/",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_role_by_id():
    role_id: str = test_create_role()
    response = client.get(
        f"{base_url}roles/{role_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get('id') == role_id
    assert response.json().get('name') == test_role_1.name


def test_update_role_by_id():
    role_id: str = test_create_role()
    response = client.put(
        f"{base_url}roles/{role_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1),
                'Content-Type': 'application/json'
        },
        json={'name': 'new_name'}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get('id') == role_id
    assert response.json().get('name') == 'new_name'


def test_delete_role():
    role_id: str = test_create_role()
    response = client.delete(
        f"{base_url}roles/{role_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 204
    response = client.get(
        f"{base_url}roles/{role_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 404


def test_create_group():
    prepare_db_with_users(test_superuser_1, test_user_1)
    response = client.post(
        f"{base_url}groups/",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        },
        data=test_group_1.json()
    )
    assert response.status_code == 201
    assert response.json().get('id')
    return response.json().get('id')


def test_get_all_groups():
    test_create_group()
    response = client.get(
        f"{base_url}groups/",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_group_by_id():
    group_id: str = test_create_group()
    response = client.get(
        f"{base_url}groups/{group_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get('id') == group_id
    assert response.json().get('name') == test_group_1.name


def test_update_group_by_id():
    group_id: str = test_create_group()
    response = client.put(
        f"{base_url}groups/{group_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1),
                'Content-Type': 'application/json'
        },
        json={'name': 'new_name'}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get('id') == group_id
    assert response.json().get('name') == 'new_name'


def test_delete_group():
    group_id: str = test_create_group()
    response = client.delete(
        f"{base_url}groups/{group_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 204
    response = client.get(
        f"{base_url}groups/{group_id}",
        headers={
                'Authorization': authenticate_as(test_superuser_1)
        }
    )
    assert response.status_code == 404
