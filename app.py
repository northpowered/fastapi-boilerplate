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
    from utils import events
    from configuration import config
    __title__ = "FastAPI boilerplate"
    __doc__ = "Your project description"
    __version__ = "1.0.0"
    __doc_url__ = config.main.doc_url
    __redoc_url__ = config.main.redoc_url

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
    )

    @app.on_event("startup")
    async def startup_event():
        app.add_middleware(PrometheusMiddleware)
        if config.telemetry.is_active:
            enable_tracing(app)
        events.load_endpoints(app)
        if config.admin_gui.is_admin_gui_enable:
            events.create_admin_gui(
                app=app,
                admin_url=config.admin_gui.admin_url,
                site_name=__title__
            )
        await events.init_vault()
        await events.load_vault_db_creds()
        await events.load_endpoint_permissions(app)

    @app.on_event("shutdown")
    async def shutdown_event():
        pass

    return app


#app = create_app()
