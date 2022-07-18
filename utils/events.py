
def load_endpoints(app):
    from accounting.routing import user_router, role_router, group_router
    from accounting.authentication.routing import auth_router
    from utils.routing import misc_router

    app.include_router(user_router)
    app.include_router(role_router)
    app.include_router(group_router)
    app.include_router(auth_router)
    app.include_router(misc_router)
    
def create_admin_gui(app, admin_url: str, site_name: str):
    from piccolo_admin.endpoints import create_admin
    from fastapi import routing
    from accounting.models import User, Role, Group, Permission, Policy
    from accounting.authentication.models import Sessions
    app.routes.append(
    routing.Mount(
        admin_url,
        create_admin(
            [
                User, 
                Role, 
                Group, 
                Permission, 
                Policy
            ],
            auth_table=User, # type: ignore
            session_table=Sessions,
            allowed_hosts=['localhost'],
            production=False,
            site_name=site_name
        )
    )
)


async def init_vault():
    from . import vault
    await vault.init()
    

async def load_vault_db_creds():
    from . import vault
    from configuration import config
    from loguru import logger
    if config.database.is_vault_enable:
        logger.debug('Using Vault for DB credentials')
        creds = await vault.get_db_creds(
                config.database.db_vault_role,
                static=config.database.is_vault_static,
                storage_name=config.database.db_vault_storage
        )
        config.database.set_connection_string(
            config.database.build_connection_string(username=creds.username,password=creds.password)
        )
        #config.database.connection_string = 
        logger.debug(f'DB engine will be created from user {creds.username}')
    else:
        config.database.set_connection_string(
            config.database.build_connection_string()
        )
        
async def reload_db_creds():
    from . import vault
    from configuration import config
    from loguru import logger
    creds = await vault.get_db_creds(
                config.database.db_vault_role,
                static=config.database.is_vault_static,
                storage_name=config.database.db_vault_storage
        )
    logger.info(f'Obtained new DB credentials from Vault for {creds.username}')
    config.database.set_connection_string(
        config.database.build_connection_string(username=creds.username,password=creds.password)
    )