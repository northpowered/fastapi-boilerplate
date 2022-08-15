from utils.api_versioning import APIRouter, APIVersion
from . import endpoints
from .jwt import oauth2_scheme
from .schemas import (
    Token
)
from fastapi.security import OAuth2PasswordRequestForm
from accounting.schemas import UserRead
from fastapi import Depends
auth_router = APIRouter(
    prefix="/auth",
    tags=["AAA->Authentication"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
        },
    #version=APIVersion(1)
)

auth_router.add_api_route(
    '/token', 
    endpoints.login_for_access_token, 
    response_model=Token,
    summary='Authenticate via JWT Bearer scheme', 
    methods=['post'],
    #dependencies=[Depends(OAuth2PasswordRequestForm)]
    )

auth_router.add_api_route(
    '/me', 
    endpoints.get_current_user, 
    response_model=UserRead,
    summary='Get current user', 
    methods=['get']
    )