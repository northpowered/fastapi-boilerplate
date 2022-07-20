from loguru import logger
from .models import Group
from accounting.schemas import (
    GroupCreate,
    GroupUpdate
)
from fastapi import Request, Response

class GroupCRUD():
    
    @staticmethod
    async def get_all_groups(request: Request, offset: int = 0, limit: int = 100):
        """
        ### READ list[Group] with offset and limit
        #### Args:\n
            offset (int, optional): Defaults to 0.\n
            limit (int, optional): Defaults to 100.\n
        #### Returns:
            list[Group]
        """
        return await Group.get_all(offset=offset,limit=limit)
    @staticmethod
    async def get_group(id: str):
        """
        ### READ one {Group} by id
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
            Group | None
        """
        return await Group.get_by_id(id)

    @staticmethod
    async def create_group(user: GroupCreate):
        """
        ### CREATE group
        #### Args:\n
            group (Group): {
                name: str (Unique)
                active: bool = True
            }
        #### Returns:
            Group
        """
        return await Group.add(**user.dict())

    @staticmethod
    async def update_group(id: str, group: GroupUpdate):
        """
        ### Update one group (full or partial)
        Args:\n
            group (Group): {
                name: str (Unique)
                active: bool
            }
        Returns:
            Group
        """
        return await Group.update_by_id(id = id, data = group.dict(exclude_unset=True))

    @staticmethod
    async def delete_group(id: str):
        """
        ### DELETE one group by ID
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
        None, code=204
        """
        await Group.delete_by_id(id)
        return Response(status_code=204)

