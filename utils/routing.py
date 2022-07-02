from fastapi import APIRouter
from starlette_exporter import handle_metrics





misc_router = APIRouter(
    prefix="",
    tags=["Misc"],
    responses={404: {"description": "URL not found"}},
)
misc_router.add_api_route("/metrics", handle_metrics,summary='Prometeus metrics',description='Metrics from starlette_exporter module')
