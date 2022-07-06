import os


def run_app(config_file: str, reload: bool):
    import uvicorn
    import os
    os.environ['X-FA-CONF-FILE'] = config_file
    from configuration import config

    uvicorn.run(
        "app:app",
        reload=reload, 
        host=config.server.bind_address,
        port=config.server.bind_port,

        )