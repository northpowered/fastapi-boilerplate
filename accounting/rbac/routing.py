from fastapi import APIRouter, Depends, HTTPException
from .endpoints import UserRoleCRUD
from accounting.users.schemas import UserRead
userRole_router = APIRouter(
    prefix="/accounting/rbac",
    tags=["AAA->Accounting->RBAC"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
        },
)

userRole_router.add_api_route(
    '/user/', 
    UserRoleCRUD.add_roles_to_user, 
    response_model=UserRead,
    summary='Add roles to user', 
    methods=['put'])