from fastapi import Depends
from utils.api_versioning import APIRouter, APIVersion
from .endpoints import (
    UserRoleCRUD,
    UserGroupCRUD,
    PermissionCRUD,
    PolicyCRUD
)
from accounting.schemas import (
    UserRead,
    RoleRead,
    GroupRead,
    PermissionRead,
    PolicyRead
)
from accounting.authentication.jwt import get_user_by_token

rbac_user_router = APIRouter(
    prefix="/accounting/rbac/user",
    tags=["AAA->Accounting->RBAC->User"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
    },
    dependencies=[Depends(get_user_by_token)],
    version=APIVersion(1)
)

rbac_role_router = APIRouter(
    prefix="/accounting/rbac/role",
    tags=["AAA->Accounting->RBAC->Role"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
    },
    dependencies=[Depends(get_user_by_token)],
    version=APIVersion(1)
)

rbac_group_router = APIRouter(
    prefix="/accounting/rbac/group",
    tags=["AAA->Accounting->RBAC->Group"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
    },
    dependencies=[Depends(get_user_by_token)],
    version=APIVersion(1)
)

rbac_permissions_router = APIRouter(
    prefix="/accounting/rbac/permissions",
    tags=["AAA->Accounting->RBAC->Permissions"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
    },
    dependencies=[Depends(get_user_by_token)],
    version=APIVersion(1)
)

rbac_policies_router = APIRouter(
    prefix="/accounting/rbac/policies",
    tags=["AAA->Accounting->RBAC->Policies"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
    },
    dependencies=[Depends(get_user_by_token)],
    version=APIVersion(1)
)

rbac_user_router.add_api_route(
    '/roles/',
    UserRoleCRUD.add_roles_to_user,
    response_model=UserRead,
    summary='Add roles to user',
    methods=['put'])

rbac_user_router.add_api_route(
    '/roles/',
    UserRoleCRUD.delete_roles_from_user,
    response_model=UserRead,
    summary='Remove roles from user',
    methods=['patch'])

rbac_user_router.add_api_route(
    '/groups/',
    UserGroupCRUD.add_groups_to_user,
    response_model=UserRead,
    summary='Add groups to user',
    methods=['put'])

rbac_user_router.add_api_route(
    '/groups/',
    UserGroupCRUD.delete_groups_from_user,
    response_model=UserRead,
    summary='Remove groups from user',
    methods=['patch'])

rbac_role_router.add_api_route(
    '/users/',
    UserRoleCRUD.add_users_to_role,
    response_model=RoleRead,
    summary='Add users to role',
    methods=['put'])

rbac_role_router.add_api_route(
    '/users/',
    UserRoleCRUD.delete_users_from_role,
    response_model=RoleRead,
    summary='Remove users from role',
    methods=['patch'])

rbac_group_router.add_api_route(
    '/users/',
    UserGroupCRUD.add_users_to_group,
    response_model=GroupRead,
    summary='Add users to group',
    methods=['put'])

rbac_group_router.add_api_route(
    '/users/',
    UserGroupCRUD.delete_users_from_group,
    response_model=GroupRead,
    summary='Remove users from group',
    methods=['patch'])

rbac_permissions_router.add_api_route(
    '/',
    PermissionCRUD.get_all_permissions,
    response_model=list[PermissionRead],
    summary='Get all permissions',
    methods=['get'])

rbac_permissions_router.add_api_route(
    '/{id}',
    PermissionCRUD.get_permission,
    response_model=PermissionRead,
    summary='Get permission by id',
    methods=['get'])

rbac_policies_router.add_api_route(
    '/',
    PolicyCRUD.get_all_policies,
    response_model=list[PolicyRead],
    summary='Get all policies',
    methods=['get'])

rbac_policies_router.add_api_route(
    '/{id}',
    PolicyCRUD.get_policy,
    response_model=PolicyRead,
    summary='Get policy by id',
    methods=['get'])

rbac_policies_router.add_api_route(
    '/',
    PolicyCRUD.add_policy,
    response_model=PolicyRead,
    status_code=201,
    summary='Create policy',
    methods=['post'])

rbac_policies_router.add_api_route(
    '/{id}',
    PolicyCRUD.update_policy,
    response_model=PolicyRead,
    summary='Update policy (full or partial)',
    methods=['put'])

rbac_policies_router.add_api_route(
    '/{id}',
    PolicyCRUD.delete_policy,
    status_code=204,
    summary='Delete policy',
    methods=['delete'])
