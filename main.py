import typer
from cli import db_app, aaa_app

app = typer.Typer(no_args_is_help=True)
app.add_typer(db_app,name='db')
app.add_typer(aaa_app,name='aaa')
@app.command()
def run(
        config: str = typer.Argument(
            'config.toml',
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



if __name__ == "__main__":
    app()
