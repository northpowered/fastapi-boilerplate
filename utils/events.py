
from loguru import logger


def load_endpoints(app):
    from accounting.routing import user_router, auth_router
    from utils.routing import misc_router

    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(misc_router)
    