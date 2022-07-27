import typer
from accounting.users.models import User
import asyncio
from fastapi.exceptions import HTTPException
async def create_superuser(username: str, password: str, email: str = str()):
    return await User.add(username,password,email, as_superuser=True)



app = typer.Typer(
    no_args_is_help=True,
    short_help='Operations with users and other AAA objects'
)


@app.command(short_help='Creating objects')
def create(object: str):
    """
    Objects:

        - superuser
    """
    match object:
        case 'superuser':
            username = typer.prompt("Username")
            password = typer.prompt("Password")
            email = typer.prompt("Email")
            try:
                resp: User = asyncio.run(create_superuser(username,password,email))
            except HTTPException as ex:
                print('Operation failed')
            else:
                print(f'Superuser {username} was created with id {resp.id}')
        case _:
            print(f"init!")

if __name__ == "__main__":
    app()