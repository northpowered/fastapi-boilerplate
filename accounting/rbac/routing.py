from fastapi import APIRouter, Depends, HTTPException
from .endpoints import UserRoleCRUD
from accounting.schemas import UserRead, RoleRead
userRole_router = APIRouter(
    prefix="/accounting/rbac",
    tags=["AAA->Accounting->RBAC"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
        },
)

userRole_router.add_api_route(
    '/user/roles/', 
    UserRoleCRUD.add_roles_to_user, 
    response_model=UserRead,
    summary='Add roles to user', 
    methods=['put'])

userRole_router.add_api_route(
    '/user/roles/', 
    UserRoleCRUD.delete_roles_from_user, 
    response_model=UserRead,
    summary='Remove roles from user', 
    methods=['patch'])


userRole_router.add_api_route(
    '/role/users/', 
    UserRoleCRUD.add_users_to_role, 
    response_model=RoleRead,
    summary='Add users to role', 
    methods=['put'])