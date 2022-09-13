from cli.config_loader import set_config
import uvicorn


def run_app(config_file: str, reload: bool):
    """
    Runs application with Uvicorn
    Application defined in app.py
    Method set_config() MUST be invoked before importing
    `config` from `configuration` module to set env var with config filename

    Args:
        config_file (str): path to config file
        reload (bool): watch file changes and reload server (useful for development)
    """
    set_config(config_file, remove_logger=False)
    from configuration import config
    uvicorn.run(
        "app:app",
        reload=reload,
        host=config.Server.bind_address,
        port=config.Server.bind_port,
    )
