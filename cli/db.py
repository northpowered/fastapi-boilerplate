import typer
import asyncio
from .config_loader import set_config, config_default
app = typer.Typer(no_args_is_help=True,short_help='Operations with DB')

migrations_app = typer.Typer(short_help='DB migrations',no_args_is_help=True)

app.add_typer(migrations_app,name='migrations')

@app.command()
def init():
    print(f"init!")


@app.command()
def drop():
    print(f"drop!")

@migrations_app.command(help='Creates migrations without running')
def create(app_name: str, c: str = typer.Option('config.ini')):
    set_config(c)
    from piccolo.apps.migrations.commands.new import new
    asyncio.run(
        new(
        app_name=app_name,
        auto=True
        )
    )

@migrations_app.command(help='Runs created migrations')
def run(
    app_name: str = typer.Argument('all'),
    c: str = config_default,
    m: str = typer.Option('all',help='Migration id to run'),
    fake: bool = typer.Option(False,is_flag=True,help='Runs migrations in FAKE mode')
    )->None:
    set_config(c)
    from piccolo.apps.migrations.commands.forwards import run_forwards
    from piccolo_conf import APP_REGISTRY
    apps: list = list()
    if app_name == 'all':
        apps = APP_REGISTRY.apps
    else:
        apps.append(app_name)
    for app in apps:
        app_name = app.rstrip('.piccolo_app')
        asyncio.run(
            run_forwards(
                app_name=app_name,
                migration_id=m,
                fake=fake
            )
        )
        
if __name__ == "__main__":
    app()