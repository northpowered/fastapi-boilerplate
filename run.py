def run_app(config_file: str, reload: bool):
    import uvicorn
    from configuration import config
    config.load(config_file)
    uvicorn.run(
        "app:app",
        reload=reload, 
        host=config.server.bind_address,
        port=config.server.bind_port
        )