from fastapi import FastAPI, routing
from configuration import config
from starlette_exporter import PrometheusMiddleware
from utils.logger import setup_logging
from utils.telemetry import enable_tracing
from utils import events
from piccolo_admin.endpoints import create_admin
from accounting.models import User
__title__ = "FastAPI boilerplate"
__doc__ = "Your project description"
__version__ = "0.0.1"
__doc_url__ = "/doc"
__redoc_url__ = "/redoc"

setup_logging()
from loguru import logger
from utils import vault #, events

app = FastAPI(
    title=__title__, 
    description=__doc__,
    version=__version__, 
    redoc_url=__redoc_url__, 
    docs_url=__doc_url__,
)
app.routes.append(
    routing.Mount(
        '/admin/',
        create_admin(
            [User]
        )
    )
)

@app.on_event("startup")
async def startup_event():
    app.add_middleware(PrometheusMiddleware)
    if config.telemetry.is_active:
        enable_tracing(app)
    events.load_endpoints(app)

@app.on_event("shutdown")
async def shutdown_event():
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        reload=True, 
        host=config.server.bind_address,
        port=config.server.bind_port
        )