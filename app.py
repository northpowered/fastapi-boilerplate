from fastapi import FastAPI as _FastAPI

class FastAPI(_FastAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

def create_app() -> FastAPI:
    """
    Creates and returns FastAPI application object
    Loads all configuration and executes events

    Returns:
        FastAPI: app object
    """
    from starlette_exporter import PrometheusMiddleware
    from utils.logger import setup_logging
    from utils.telemetry import enable_tracing
    from utils.id_propagation import IDPropagationMiddleware
    from utils import events
    from configuration import config
    __title__ = "FastAPI boilerplate"
    __doc__ = "Your project description"
    __version__ = "1.0.0"
    __doc_url__ = config.Main.doc_url
    __redoc_url__ = config.Main.redoc_url

    # You should import logger from loguru after setup_logging()
    # for right logger initialization
    setup_logging()
    from loguru import logger

    app = FastAPI(
        title=__title__,
        description=__doc__,
        version=__version__,
        redoc_url=__redoc_url__,
        docs_url=__doc_url__,
        #swagger_ui_init_oauth={"realm":"qqq"}

    )

    @app.on_event("startup")
    async def startup_event():
        app.add_middleware(PrometheusMiddleware)
        app.add_middleware(IDPropagationMiddleware)
        if config.Telemetry.is_active:
            enable_tracing(app)
        events.load_endpoints(app)
        if config.AdminGUI.is_admin_gui_enable:
            events.create_admin_gui(
                app=app,
                admin_url=config.AdminGUI.admin_url,
                site_name=__title__
            )
        await events.init_vault()
        await events.load_vault_db_creds()
        await events.load_endpoint_permissions(app)
        await events.load_base_jwt_secret()
        #print('test')
        from utils import vault
        #q = await vault._action('read','/kv/data/jwt')
        q = await vault.read_kv_data('jwt')
        print(q)
        pl: dict = {'data':{'secret':'bar'}}
        await vault.write_kv_data('jwt',pl)

        config.Security.set_jwt_base_secret('fwefqwefwefwqf')
        print(config.Security.get_jwt_base_secret())
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.warning('Application is shutting down')

    return app

app = create_app()
