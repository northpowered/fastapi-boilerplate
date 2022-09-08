from loguru import logger
from .models import Group
from accounting.schemas import (
    GroupCreate,
    GroupUpdate
)
from fastapi import Request, Response
from accounting.decorators import AAA_endpoint_oauth2


class GroupCRUD():

    @staticmethod
    @AAA_endpoint_oauth2()
    async def get_all_groups(request: Request, offset: int = 0, limit: int = 100):
        """
        ### READ list[Group] with offset and limit
        #### Args:\n
            offset (int, optional): Defaults to 0.\n
            limit (int, optional): Defaults to 100.\n
        #### Returns:
            list[Group]
        """
        return await Group.get_all(offset=offset, limit=limit)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def get_group(request: Request, id: str = str()):
        """
        ### READ one {Group} by id
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
            Group | None
        """
        return await Group.get_by_id(id)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def create_group(request: Request, user: GroupCreate):
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
    @AAA_endpoint_oauth2()
    async def update_group(request: Request, id: str, group: GroupUpdate):
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
        return await Group.update_by_id(id=id, data=group.dict(exclude_unset=True))

    @staticmethod
    @AAA_endpoint_oauth2()
    async def delete_group(request: Request, id: str):
        """
        ### DELETE one group by ID
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
        None, code=204
        """
        await Group.delete_by_id(id)
        return Response(status_code=204)
