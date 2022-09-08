from loguru import logger


def load_endpoints(app):
    from accounting import (
        user_router,
        role_router,
        group_router,
        rbac_user_router,
        rbac_permissions_router,
        rbac_group_router,
        rbac_policies_router,
        rbac_role_router
    )
    from accounting.authentication.routing import auth_router
    from utils.routing import misc_router

    app.include_router(user_router)
    app.include_router(role_router)
    app.include_router(group_router)
    app.include_router(auth_router)
    app.include_router(rbac_user_router)
    app.include_router(rbac_role_router)
    app.include_router(rbac_group_router)
    app.include_router(rbac_permissions_router)
    app.include_router(rbac_policies_router)
    app.include_router(misc_router)


def create_admin_gui(app, admin_url: str, site_name: str):
    from piccolo_admin.endpoints import create_admin
    from fastapi import routing
    from accounting import User, Role, Group, Permission, Policy, Sessions, M2MUserRole, M2MUserGroup
    app.routes.append(
        routing.Mount(
            admin_url,
            create_admin(
                [
                    User,
                    Role,
                    Group,
                    Permission,
                    Policy,
                    M2MUserGroup,
                    M2MUserRole
                ],
                auth_table=User,  # type: ignore
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
    if config.Database.is_vault_enable:
        logger.info('Using Vault for DB credentials')
        creds = await vault.get_db_creds(
            config.Database.db_vault_role,
            static=config.Database.is_vault_static,
            storage_name=config.Database.db_vault_storage
        )
        config.Database.set_connection_string(
            config.Database.build_connection_string(
                username=creds.username, password=creds.password)
        )
        logger.debug(f'DB engine will be created from user {creds.username}')
    else:
        config.Database.set_connection_string(
            config.Database.build_connection_string()
        )


async def reload_db_creds():
    from . import vault
    from configuration import config
    from loguru import logger
    creds = await vault.get_db_creds(
        config.Database.db_vault_role,
        static=config.Database.is_vault_static,
        storage_name=config.Database.db_vault_storage
    )
    logger.info(f'Obtained new DB credentials from Vault for {creds.username}')
    config.Database.set_connection_string(
        config.Database.build_connection_string(
            username=creds.username, password=creds.password)
    )


async def load_endpoint_permissions(app):
    from accounting import Permission
    from accounting.schemas import PermissionCreate
    from loguru import logger
    BASE_PERMISSIONS = list()
    for r in app.routes:
        try:
            BASE_PERMISSIONS.append(
                PermissionCreate(
                    object=r.endpoint.__name__,
                    name=r.summary,
                    description=r.endpoint.__doc__
                )
            )
            if r.endpoint.__getattribute__('rbac_enable'):
                r.summary = f'{r.summary} | RBAC enabled'
        except AttributeError:
            continue
    (existing_permissions, inserted_permissons) = await Permission.add_from_list(BASE_PERMISSIONS)
    logger.info(
        f"Base permissions were loaded. {inserted_permissons} entries were inserted, {existing_permissions} entries were existed"
    )


async def load_base_jwt_secret():
    from . import vault
    from configuration import config
    # if secret is defined in config file with `jwt_base_secret =`
    # we will use this one
    if config.Security.jwt_base_secret:
        return
    # or trying to load it from external storage
    match config.Security.jwt_base_secret_storage:
        case 'local':
            try:
                with open(config.Security.jwt_base_secret_filename, 'r') as f:
                    key: str = f.readline()
                    assert key, 'File is empty!'
                    config.Security.set_jwt_base_secret(key)
            except (FileNotFoundError, PermissionError):
                logger.critical(
                    f"Cannot open jwt secret file {config.Security.jwt_base_secret_filename}")
            except AssertionError as ex:
                logger.critical(str(ex))
        case 'vault':
            vault_subkey: str = 'base_secret'
            try:
                resp: dict = await vault.read_kv_data(
                    secret_name=config.Security.jwt_base_secret_vault_secret_name,
                    storage_name=config.Security.jwt_base_secret_vault_storage_name
                )
                assert (resp and isinstance(resp, dict)
                        ), "Cannot load secret from Vault"
                key: str | None = resp.get(vault_subkey)
                assert key, f"{vault_subkey} not found"
                config.Security.set_jwt_base_secret(key)
            except AssertionError as ex:
                logger.critical(str(ex))
        case _:
            logger.critical("Cannot load jwt secret")
