import typer
import asyncio
from enum import Enum
from fastapi.exceptions import HTTPException
from .config_loader import set_config, config_default
from asyncpg.exceptions import PostgresError
from loguru import logger
from email_validator import validate_email, EmailUndeliverableError
import os
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

@app.command(short_help='Creating objects', no_args_is_help=True)
def create(object: CreatingObjects, c: str = typer.Option('config.ini')):
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
        case _:
            pass

if __name__ == "__main__":
    app()