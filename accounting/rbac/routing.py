from fastapi import APIRouter, Depends, HTTPException
from .endpoints import UserRoleCRUD, UserGroupCRUD
from accounting.schemas import UserRead, RoleRead, GroupRead
rbac_router = APIRouter(
    prefix="/accounting/rbac",
    tags=["AAA->Accounting->RBAC"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
        },
)

rbac_router.add_api_route(
    '/user/roles/', 
    UserRoleCRUD.add_roles_to_user, 
    response_model=UserRead,
    summary='Add roles to user', 
    methods=['put'])

rbac_router.add_api_route(
    '/user/roles/', 
    UserRoleCRUD.delete_roles_from_user, 
    response_model=UserRead,
    summary='Remove roles from user', 
    methods=['patch'])

rbac_router.add_api_route(
    '/role/users/', 
    UserRoleCRUD.add_users_to_role, 
    response_model=RoleRead,
    summary='Add users to role', 
    methods=['put'])

rbac_router.add_api_route(
    '/role/users/', 
    UserRoleCRUD.delete_users_from_role, 
    response_model=RoleRead,
    summary='Remove users from role', 
    methods=['patch'])

rbac_router.add_api_route(
    '/user/groups/', 
    UserGroupCRUD.add_groups_to_user, 
    response_model=UserRead,
    summary='Add groups to user', 
    methods=['put'])

rbac_router.add_api_route(
    '/user/groups/', 
    UserGroupCRUD.delete_groups_from_user, 
    response_model=UserRead,
    summary='Remove groups from user', 
    methods=['patch'])

rbac_router.add_api_route(
    '/group/users/', 
    UserGroupCRUD.add_users_to_group, 
    response_model=GroupRead,
    summary='Add users to group', 
    methods=['put'])

rbac_router.add_api_route(
    '/group/users/', 
    UserGroupCRUD.delete_users_from_group, 
    response_model=GroupRead,
    summary='Remove users from group', 
    methods=['patch'])