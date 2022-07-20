from loguru import logger
from .models import Role
from accounting.schemas import (
    RoleCreate,
    RoleUpdate,
)
from fastapi import Request, Response

class RoleCRUD():
    
    @staticmethod
    async def get_all_roles(request: Request, offset: int = 0, limit: int = 100):
        """
        ### READ list[Role] with offset and limit
        #### Args:\n
            offset (int, optional): Defaults to 0.\n
            limit (int, optional): Defaults to 100.\n
        #### Returns:
            list[Role]
        """
        return await Role.get_all(offset=offset,limit=limit)
    @staticmethod
    async def get_role(id: str):
        """
        ### READ one {Role} by id
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
            Role | None
        """
        return await Role.get_by_id(id)
    @staticmethod
    async def create_role(user: RoleCreate):
        """
        ### CREATE role
        #### Args:\n
            role (Role): {
                name: str (Unique)
                active: bool = True
            }
        #### Returns:
            Role
        """
        return await Role.add(**user.dict())
    @staticmethod
    async def update_role(id: str, role: RoleUpdate):
        """
        ### Update one role (full or partial)
        Args:\n
            role (Role): {
                name: str (Unique)
                active: bool
            }
        Returns:
            Role
        """
        return await Role.update_by_id(id = id, data = role.dict(exclude_unset=True))

    @staticmethod
    async def delete_role(id: str):
        """
        ### DELETE one role by ID
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
        None, code=204
        """
        await Role.delete_by_id(id)
        return Response(status_code=204)