from fastapi import Request, Response
from .schemas import RolesToUser

class RbacCRUD():

    @staticmethod
    async def link_user_to_roles(request: Request, data: RolesToUser):
        pass
