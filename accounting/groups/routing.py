from fastapi import APIRouter, Depends, HTTPException
from .endpoints import GroupCRUD
from accounting.schemas import (
   GroupRead
)

group_router = APIRouter(
    prefix="/accounting/groups",
    tags=["AAA->Accounting->Groups"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"}
        },
)

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
    response_model=GroupRead,
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
