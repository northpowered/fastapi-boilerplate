from fastapi import APIRouter, Depends, HTTPException
from .endpoints import UserCRUD, RoleCRUD, GroupCRUD
from .schemas import (
   UserRead,
   UserCreate,
   UserUpdate,
   UserPasswordChange,
   RoleRead,
   GroupRead
)

user_router = APIRouter(
    prefix="/accounting/users",
    tags=["AAA->Accounting->Users"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
        },
)

role_router = APIRouter(
    prefix="/accounting/roles",
    tags=["AAA->Accounting->Roles"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
        },
)

group_router = APIRouter(
    prefix="/accounting/groups",
    tags=["AAA->Accounting->Groups"],
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


role_router.add_api_route(
    '/', 
    RoleCRUD.get_all_roles, 
    response_model=list[RoleRead], 
    summary='Get all roles',
    methods=['get']
)

role_router.add_api_route(
    '/{id}', 
    RoleCRUD.get_role, 
    response_model=RoleRead, 
    summary='Get role by ID pk',
    methods=['get']
)

role_router.add_api_route(
    '/', 
    RoleCRUD.create_role, 
    response_model=RoleRead,
    status_code=201, 
    summary='Create role', 
    methods=['post'])

role_router.add_api_route(
    '/{id}', 
    RoleCRUD.update_role, 
    response_model=RoleRead,
    summary='Update role', 
    methods=['put'])

role_router.add_api_route(
    '/{id}', 
    RoleCRUD.delete_role,
    status_code=204,
    summary='Delete role', 
    methods=['delete'])

group_router.add_api_route(
    '/', 
    GroupCRUD.get_all_groups, 
    response_model=list[GroupRead], 
    summary='Get all groups',
    methods=['get']
)

group_router.add_api_route(
    '/{id}', 
    GroupCRUD.get_group, 
    response_model=GroupRead, 
    summary='Get group by ID pk',
    methods=['get']
)

group_router.add_api_route(
    '/', 
    GroupCRUD.create_group, 
    response_model=RoleRead,
    status_code=201, 
    summary='Create group', 
    methods=['post'])

group_router.add_api_route(
    '/{id}', 
    GroupCRUD.update_group, 
    response_model=GroupRead,
    summary='Update group', 
    methods=['put'])

group_router.add_api_route(
    '/{id}', 
    GroupCRUD.delete_group,
    status_code=204,
    summary='Delete group', 
    methods=['delete'])
