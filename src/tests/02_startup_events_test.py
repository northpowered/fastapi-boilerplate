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


def test_load_base_jwt_secret():
    from utils.events import load_base_jwt_secret
    asyncio.run(load_base_jwt_secret())
