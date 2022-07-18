from fastapi import APIRouter, Depends, HTTPException
from .endpoints import UserCRUD
from .schemas import (
   UserRead,
   UserCreate,
   UserUpdate,
   UserPasswordChange,
)
user_router = APIRouter(
    prefix="/accounting/users",
    tags=["AAA->Accounting->Users"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
        },
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
