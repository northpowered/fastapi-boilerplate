import os


def run_app(config_file: str, reload: bool):
    import uvicorn #mypy
    import os
    from app import create_app
    os.environ['X_FA_CONF_FILE'] = config_file
    from configuration import config
    from utils.logger import setup_logging
    setup_logging()
    from loguru import logger
    app = create_app()
    uvicorn.run(
        app,
        reload=reload, 
        host=config.server.bind_address,
        port=config.server.bind_port,

        )