from fastapi import Depends
from .endpoints import UserCRUD
from accounting.schemas import (
    UserRead,
)
from accounting.authentication.jwt import get_user_by_token
from utils.api_versioning import APIRouter, APIVersion
user_router = APIRouter(
    prefix="/accounting/users",
    tags=["AAA->Accounting->Users"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
    },
    dependencies=[Depends(get_user_by_token)],
    version=APIVersion(1)
)

user_router.add_api_route(
    '/',
    UserCRUD.get_all_users,
    response_model=list[UserRead],
    summary='Get all users',
    methods=['get']
)

user_router.add_api_route(
    '/{id}',
    UserCRUD.get_user,
    response_model=UserRead,
    summary='Get user by ID pk',
    methods=['get']
)

user_router.add_api_route(
    '/',
    UserCRUD.create_user,
    response_model=UserRead,
    status_code=201,
    summary='Create user',
    methods=['post'])

user_router.add_api_route(
    '/{id}',
    UserCRUD.update_user,
    response_model=UserRead,
    summary='Update user',
    methods=['put'])

user_router.add_api_route(
    '/{id}',
    UserCRUD.patch_user,
    response_model=UserRead,
    summary='Change user password',
    methods=['patch'])

user_router.add_api_route(
    '/{id}',
    UserCRUD.delete_user,
    status_code=204,
    summary='Delete user',
    methods=['delete'])
