from fastapi import Depends
from utils.api_versioning import APIRouter, APIVersion
from .endpoints import RoleCRUD
from accounting.schemas import (
   RoleRead,
)
from accounting.authentication.jwt import get_user_by_token

role_router = APIRouter(
    prefix="/accounting/roles",
    tags=["AAA->Accounting->Roles"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
        },
    dependencies=[Depends(get_user_by_token)],
    version=APIVersion(1)
)

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