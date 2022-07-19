from fastapi import Request, Response
from .schemas import RolesToUser, RoleToUser, UsersToRole
from accounting import Role, User
class UserRoleCRUD():

    @staticmethod
    async def get_roles_of_user(request: Request, user_id: str):
        pass

    @staticmethod
    async def get_users_of_role(request: Request, role_id: str):
        pass

    @staticmethod
    async def add_roles_to_user(request: Request, data: RolesToUser):
        resp =  await User.add_roles(user_id=data.user_id,role_ids=data.role_ids)
        print(resp)
        return resp

    @staticmethod
    async def add_role_to_user(request: Request, data: RoleToUser):
        pass

    @staticmethod
    async def add_users_to_role(request: Request, data: UsersToRole):
        pass

    @staticmethod
    async def delete_roles_to_user(request: Request, data: RolesToUser):
        pass

    @staticmethod
    async def delete_role_to_user(request: Request, data: RoleToUser):
        pass

    @staticmethod
    async def delete_users_to_role(request: Request, data: UsersToRole):
        pass