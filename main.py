import typer
from cli import db_app
app = typer.Typer(no_args_is_help=True)

@app.command()
def run(
        config: str = typer.Argument(
            'config.ini',
            help="Path to config file"
        ),
        reload: bool = typer.Option(
            False,
            is_flag=True, 
            flag_value=True,
            help="Allow Uvicorn watch file changes and reload server"
        )
    ):
    """ 
    Run application in uvicorn server with defined config file
    """
    from run import run_app
    run_app(
        config_file=config,
        reload=reload
    )


app.add_typer(db_app,name='db')

if __name__ == "__main__":
    app()