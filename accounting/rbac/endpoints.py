from fastapi import Request, Response
from accounting.schemas import RolesToUser, RoleToUser, UsersToRole
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
        return await User.add_roles(user_id=data.user_id,role_ids=data.role_ids)

    @staticmethod
    async def add_users_to_role(request: Request, data: UsersToRole):
        return await Role.add_users(role_id=data.role_id, user_ids=data.user_ids)

    @staticmethod
    async def delete_roles_from_user(request: Request, data: RolesToUser):
        return await User.delete_roles(user_id=data.user_id,role_ids=data.role_ids)

    @staticmethod
    async def delete_users_from_role(request: Request, data: UsersToRole):
        pass