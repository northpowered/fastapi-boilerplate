import typer
import asyncio
app = typer.Typer(no_args_is_help=True,short_help='Operations with DB')

migrations_app = typer.Typer(short_help='DB migrations',no_args_is_help=True)

app.add_typer(migrations_app,name='migrations')

@app.command()
def init():
    print(f"init!")


@app.command()
def drop():
    print(f"drop!")

@migrations_app.command()
def create(app_name: str):
    from piccolo.apps.migrations.commands.new import new
    asyncio.run(
        new(
        app_name=app_name,
        auto=True
        )
    )

if __name__ == "__main__":
    app()