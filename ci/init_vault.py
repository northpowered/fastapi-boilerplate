import requests

URL: str = "http://127.0.0.1:8228/"
TOKEN: str = "hvs.e7zbhM4OadYPKTLqGNH9eCci"
HEADERS: dict = {'X-Vault-Token':TOKEN}

database_mount: str = "database"
kv_mount: str = "kv_test"

db_host = 'fastapi-boilerplate-postgres:5432'
db_dsn: str = f"postgresql://fastapi-boilerplate:fastapi-boilerplate@{db_host}/fastapi-boilerplate?sslmode=disable"
db_role: str = "testrole"
kv_secret_name: str = "jwt"
def post(path: str, data: dict)->requests.Response:
    return requests.post(
        url=f"{URL}{path}",
        json=data,
        headers=HEADERS
    )

""" VAULT DATABASE INIT """

print("Creating database secret engine")
resp = post(f'v1/sys/mounts/{database_mount}',{"type":"database"})
print(f"{resp.status_code} --- {resp.text}")

print("Creating database connection")
resp = post(
    path=f"v1/{database_mount}/config/postgresql",
    data={
        "plugin_name": "postgresql-database-plugin",
        "allowed_roles": "*",
        "connection_url": db_dsn,
        "username": "fastapi-boilerplate",
        "password": "fastapi-boilerplate"
    }
)
print(f"{resp.status_code} --- {resp.text}")

print("Creating static role")
resp = post(
    path=f"v1/{database_mount}/static-roles/{db_role}",
    data={
        "db_name": "postgresql",
        "rotation_statements": "ALTER USER \"{{name}}\" WITH PASSWORD '{{password}}';",
        "username": "fastapi-boilerplate",
        "rotation_period": "86400"
    }
)
print(f"{resp.status_code} --- {resp.text}")

""" VAULT KV INIT """

print("Creating KVv2 storage")
resp = post(
    path=f"v1/sys/mounts/{kv_mount}",
    data={
        "type": "kv",
        "options": {
            "version": "2"
        }
    }
)
print(f"{resp.status_code} --- {resp.text}")

print("Push something to KV")
resp = post(
    path=f"v1/{kv_mount}/data/{kv_secret_name}",
    data={
        "data": {
            "base_secret": "foobar"
        }
    }
)
print(f"{resp.status_code} --- {resp.text}")
