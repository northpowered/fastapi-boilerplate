import typer
import asyncio
from rich import print
from rich.table import Table as CLI_Table
from rich.console import Console
from .config_loader import set_config, config_default
from dataclasses import dataclass

app = typer.Typer(no_args_is_help=True,short_help='Operations with DB')
console = Console()
migrations_app = typer.Typer(short_help='DB migrations',no_args_is_help=True)
app.add_typer(migrations_app,name='mg')

@dataclass
class TableScan():
    from piccolo.table import Table  #CircularImport error
    application: str
    table: Table
    exists: bool | None = None
    action: str | None = None
    result: bool| None = None

def get_tables_list(apps: list | None = None,check_for_existance: bool = False)->list[TableScan]:
    """
    Scan APP_REGISTRY for registered tables and returns list of TableScan objects

    Args:
        apps (list | None, optional): Applications to include or ALL of them. Defaults to None.
        check_for_existance (bool, optional): Check existing in db and fill `exists` field. Defaults to False.

    Returns:
        list[TableScan]: list of scanned tables
    """
    from piccolo_conf import APP_REGISTRY
    tables: list = list()
    for app in APP_REGISTRY.apps:
        app_name: str = app.rstrip('.piccolo_app')
        if apps is not None:
            if app_name not in apps:
                continue
        app_tables: list = APP_REGISTRY.get_table_classes(
                app_name
        )
        for app_table in app_tables:
            exists: bool | None = None
            if check_for_existance:
                exists = app_table.table_exists().run_sync()
            tables.append(
                TableScan(
                    application=app_name,
                    table=app_table,
                    exists=exists
                )
            )
    return tables

@app.command(help="Show current state of tables")
def show(
    app_name: str = typer.Argument('all',help='Application name, ex. `accounting` or `all` for all registered apps'),
    c: str = config_default
    ):
    """
    Show scanned tables

    Args:
        app_name (str, optional): Specify an application. Defaults to 'all'.
    """
    set_config(c)
    apps: list[str] | None = None
    if app_name != 'all':
        apps = [app_name]
    tables: list = get_tables_list(apps=apps, check_for_existance=True)
    cli_table: CLI_Table = CLI_Table("#", "Application", "Table name", "Exists")
    counter: int = 1
    for table in tables:
        exists_str: str = ':no_entry:'
        if table.exists:
            exists_str = ':green_circle:'
        cli_table.add_row(
            str(counter), 
            table.application,
            table.table.__name__,
            exists_str,
        )
        counter = counter + 1
    console.print(cli_table)


@app.command(help="Create all or app specified tables for application, existing tables will be ignored")
def init(
    app_name: str = typer.Argument('all',help='Application name, ex. `accounting` or `all` for all registered apps'),
    c: str = config_default
    ):
    """
    Create tables from scanned apps, all or for selected application

    Args:
        app_name (str, optional): _description_. Defaults to 'all'.
    """
    set_config(c)
    from piccolo.table import create_db_tables_sync
    from piccolo_conf import APP_REGISTRY
    apps: list[str] | None = None
    if app_name != 'all':
        apps = [app_name]
    tables: list = get_tables_list(apps=apps, check_for_existance=True)
    cli_table: CLI_Table = CLI_Table("#", "Application", "Table name", "Already exists", "Action","Result")
    counter: int = 1
    for table in tables:
        if table.exists:
            table.action = "[yellow]Ignore[/yellow]"
        else:
            table.action = "[green]Create[/green]"
        create_db_tables_sync(table.table, if_not_exists=True)
        if table.table.table_exists().run_sync():
            if table.exists:
                table.result = "[green]Ignored[/green]"
            else:
                table.result = "[green]Created[/green]"
        else:
            table.result = "[red]Error[/red]"
        exists_str: str = ':no_entry:'
        if table.exists:
            exists_str = ':green_circle:'
        cli_table.add_row(
            str(counter), 
            table.application,
            table.table.__name__,
            exists_str,
            table.action,
            table.result
        )
        counter = counter + 1
    console.print(cli_table)


@app.command(help="Drop all or app specified tables for application, existing tables will be ignored")
def drop(
    app_name: str = typer.Argument('all',help='Application name, ex. `accounting` or `all` for all registered apps'),
    c: str = config_default
    ):
    """
    Drop tables from scanned apps, all or for selected application

    Args:
        app_name (str, optional): _description_. Defaults to 'all'.
    """
    set_config(c)
    from piccolo.table import drop_db_tables_sync
    from piccolo_conf import APP_REGISTRY
    apps: list[str] | None = None
    if app_name != 'all':
        apps = [app_name]
    tables: list = get_tables_list(apps=apps, check_for_existance=True)
    delete = typer.confirm(f"Are you sure you want to delete {app_name} tables?", abort=True)
    cli_table: CLI_Table = CLI_Table("#", "Application", "Table name", "Already exists", "Action","Result")
    counter: int = 1
    for table in tables:
        if table.exists:
            table.action = "[red bold]Drop[/red bold]"
        else:
            table.action = "[yellow]Ignore[/yellow]"
        drop_db_tables_sync(table.table)
        if not table.table.table_exists().run_sync():
            if table.exists:
                table.result = "[green]Dropped[/green]"
            else:
                table.result = "[green]Ignored[/green]"
        else:
            table.result = "[red]Error[/red]"
        exists_str: str = ':no_entry:'
        if table.exists:
            exists_str = ':green_circle:'
        cli_table.add_row(
            str(counter), 
            table.application,
            table.table.__name__,
            exists_str,
            table.action,
            table.result
        )
        counter = counter + 1
    console.print(cli_table)


"""Migrations commands"""
@migrations_app.command(help='Create migrations without running')
def create(
    app_name: str = typer.Argument('all',help='Application name, ex. `accounting` or `all` for all registered apps'),
    c: str = config_default
    )->None:
    set_config(c)
    from piccolo.apps.migrations.commands.new import new
    from piccolo_conf import APP_REGISTRY
    apps: list = list()
    if app_name == 'all':
        apps = APP_REGISTRY.apps
    else:
        apps.append(app_name)
    for app in apps:
        app_name = app.rstrip('.piccolo_app')
        print(f'Running for [green]{app_name}[/green] app')
        asyncio.run(
            new(
            app_name=app_name,
            auto=True
            )
        )

@migrations_app.command(help='Run created migrations')
def run(
    app_name: str = typer.Argument('all',help='Application name, ex. `accounting` or `all` for all registered apps'),
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
        print(f'Running for [green]{app_name}[/green] app')
        asyncio.run(
            run_forwards(
                app_name=app_name,
                migration_id=m,
                fake=fake
            )
        )
        
if __name__ == "__main__":
    app()