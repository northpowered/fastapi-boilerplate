from utils.api_versioning import APIRouter, APIVersion
from . import endpoints
from .schemas import (
    Token
)
from accounting.schemas import UserRead
auth_router = APIRouter(
    prefix="/auth",
    tags=["AAA->Authentication"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
    },
)

auth_router.add_api_route(
    '/token',
    endpoints.login_for_access_token,
    response_model=Token,
    summary='Authenticate via JWT Bearer scheme',
    methods=['post']
)

auth_router.add_api_route(
    '/me',
    endpoints.get_current_user,
    response_model=UserRead,
    summary='Get current user',
    methods=['get']
)
