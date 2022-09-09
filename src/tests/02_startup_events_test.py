import asyncio
from fastapi.testclient import TestClient
from app import create_app

app = create_app()
client = TestClient(app)


def test_load_endpoints():
    from utils.events import load_endpoints
    load_endpoints(app)


def test_enable_telemetry():
    from utils.telemetry import enable_tracing
    enable_tracing(app)


def test_creating_admin_gui():
    from utils.events import create_admin_gui
    create_admin_gui(app, '/admin', 'foobar')


def test_load_endpoint_permissions():
    from utils.events import load_endpoint_permissions
    from cli.db import prepare_db_through_vault
    prepare_db_through_vault()
    asyncio.run(load_endpoint_permissions(app))


def test_load_base_jwt_secret_from_config():
    from utils.events import load_base_jwt_secret
    asyncio.run(load_base_jwt_secret())


def test_load_base_jwt_secret_from_file():
    from configuration import config
    from utils.events import load_base_jwt_secret
    asyncio.run(
        load_base_jwt_secret(
            jwt_base_secret=None,
            jwt_base_secret_storage='local',
            jwt_base_secret_filename='src/tests/etc/jwt.txt'
        )
    )
    assert config.Security.get_jwt_base_secret() == 'localfilesecret'


def test_load_base_jwt_secret_from_vault():
    from configuration import config
    from utils.events import load_base_jwt_secret
    from utils.vault import Vault
    vault: Vault = Vault(
        auth=Vault.VaultAuth(
            auth_method='token',
            token='test'
        )
    )
    asyncio.run(
        load_base_jwt_secret(
            jwt_base_secret=None,
            jwt_base_secret_vault_secret_name='jwt',
            jwt_base_secret_vault_storage_name='kv_test',
            vault=vault
        )
    )
    assert isinstance(config.Security.get_jwt_base_secret(), str)
    assert len(config.Security.get_jwt_base_secret()) > 10


def test_reload_db_creds():
    from utils.events import reload_db_creds
    asyncio.run(reload_db_creds())
