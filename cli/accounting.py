import typer
import asyncio
from enum import Enum
from fastapi.exceptions import HTTPException
from .config_loader import set_config, config_default
from loguru import logger
from email_validator import validate_email, EmailUndeliverableError
from configuration import config
from .console import print
from utils import vault,events
from utils.security import generate_random_string_token
async def create_user(username: str, password: str, email: str, superuser: bool=False):
    from accounting.users.models import User
    try:
        validate_email(email,check_deliverability=False)
    except EmailUndeliverableError:
        logger.critical(f"Email {email} is not valid")
        raise HTTPException(status_code=422) # Raising HTTP error to propagate error to another thread
    else:
        return await User.add(username,password,email, as_superuser=superuser)

app = typer.Typer(
    no_args_is_help=True,
    short_help='Operations with users and other AAA objects'
)

class CreatingObjects(str, Enum):
    superuser: str = "superuser"
    user: str = "user"
    secret: str = "secret"

@app.command(short_help='Creating objects', no_args_is_help=True)
def create(object: CreatingObjects, c: str = config_default):
    """
    Creating AAA objects
    """
    set_config(c)
    match object:
        case 'superuser':
            username = typer.prompt("Username")
            password = typer.prompt("Password")
            email = typer.prompt("Email")
            try:
                resp = asyncio.run(create_user(username,password,email,True))
            except HTTPException:
                logger.error('Unable to create superuser')
            else:
                print(f'Superuser {username} was created with id {resp.id}')
        case 'user':
            username = typer.prompt("Username")
            password = typer.prompt("Password")
            email = typer.prompt("Email")
            try:
                resp = asyncio.run(create_user(username,password,email))
            except HTTPException as ex:
                logger.error('Unable to create user')
            else:
                print(f'User {username} was created with id {resp.id}')
        case 'secret':
            if config.Security.jwt_base_secret:
                print("[yellow bold]Warning![/yellow bold] jwt_base_secret is defined in config file.\
                    \n      Comment this line in [bold]Security[/bold] section to load secret from external storage")
            print(f"Using [green bold]{config.Security.jwt_base_secret_storage}[/green bold] external storage")
            new_secret: str = generate_random_string_token()
            secret_to_check: str = str()
            match config.Security.jwt_base_secret_storage:
                case 'local':
                    try:
                        with open(config.Security.jwt_base_secret_filename,'w') as f:
                            f.write(new_secret)
                            f.close()
                        with open(config.Security.jwt_base_secret_filename,'r') as f:
                           secret_to_check = f.readline()
                           config.Security.set_jwt_base_secret(secret_to_check )
                    except (FileNotFoundError, PermissionError):
                        logger.critical(f"Cannot write jwt secret to file {config.Security.jwt_base_secret_filename}")
                case 'vault':
                    asyncio.run(events.init_vault())
                    vault_subkey: str = 'base_secret'
                    try:
                        response_write: dict = asyncio.run(
                            vault.write_kv_data(
                                secret_name=config.Security.jwt_base_secret_vault_secret_name,
                                payload={'data':{vault_subkey:new_secret}},
                                storage_name=config.Security.jwt_base_secret_vault_storage_name
                            )
                        )
                        assert response_write, "Vault write operation failed"
                        response_read: dict | None = asyncio.run(
                            vault.read_kv_data(
                                secret_name=config.Security.jwt_base_secret_vault_secret_name,
                                storage_name=config.Security.jwt_base_secret_vault_storage_name
                            )
                        )
                        assert (response_read and isinstance(response_read,dict)), "Cannot load secret from Vault"
                        secret_to_check = response_read.get(vault_subkey,str())
                        config.Security.set_jwt_base_secret(secret_to_check)
                    except AssertionError as ex:
                        logger.critical(str(ex))
                case _:
                    pass
            try:
                assert new_secret == secret_to_check, "Wroted secret is broken"
                assert secret_to_check == config.Security.get_jwt_base_secret(), "Loading to CONFIG is broken"
            except AssertionError as ex:
                logger.critical(str(ex))
            else:
                print("All checks successfully passed")



        case _:
            pass

if __name__ == "__main__":
    app()