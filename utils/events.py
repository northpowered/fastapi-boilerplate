
def load_endpoints(app):
    from accounting.routing import user_router, auth_router
    from utils.routing import misc_router

    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(misc_router)
    
def create_admin_gui(app, admin_url: str, site_name: str):
    from piccolo_admin.endpoints import create_admin
    from fastapi import routing
    from accounting.models import User,Sessions
    app.routes.append(
    routing.Mount(
        admin_url,
        create_admin(
            [User],
            auth_table=User,
            session_table=Sessions,
            allowed_hosts=['localhost'],
            production=False,
            site_name=site_name
        )
    )
)


def startup(app):
    from starlette_exporter import PrometheusMiddleware
    from utils.telemetry import enable_tracing
    from configuration import config

    app.add_middleware(PrometheusMiddleware)
    if config.telemetry.is_active:
        enable_tracing(app)
    load_endpoints(app)
    if config.admin_gui.is_admin_gui_enable:
        create_admin_gui(
            app=app,
            admin_url=config.admin_gui.admin_url,
            site_name=app.title
        )

def shutdown(app):
    pass