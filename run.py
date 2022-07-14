import os


def run_app(config_file: str, reload: bool):
    import uvicorn #mypy
    import os
    os.environ['X_FA_CONF_FILE'] = config_file
    from configuration import config

    uvicorn.run(
        "app:app",
        reload=reload, 
        host=config.server.bind_address,
        port=config.server.bind_port,

        )