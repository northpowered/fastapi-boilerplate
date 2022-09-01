import asyncio


def prepare_db_through_vault():
    from utils.events import load_vault_db_creds
    from utils import vault
    asyncio.run(vault.init())
    asyncio.run(load_vault_db_creds())
