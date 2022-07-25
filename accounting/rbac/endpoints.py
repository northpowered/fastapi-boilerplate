from fastapi import Request, Response
from accounting.schemas import RolesToUser, UsersToRole, UsersToGroup, GroupesToUser
from accounting import Role, User, Group
class UserRoleCRUD():

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
        return await Role.delete_users(role_id=data.role_id, user_ids=data.user_ids)

class UserGroupCRUD():

    @staticmethod
    async def add_groups_to_user(request: Request, data: GroupesToUser):
        return await User.add_groups(user_id=data.user_id,group_ids=data.group_ids)

    @staticmethod
    async def add_users_to_group(request: Request, data: UsersToGroup):
        return await Group.add_users(group_id=data.group_id, user_ids=data.user_ids)

    @staticmethod
    async def delete_groups_from_user(request: Request, data: GroupesToUser):
        return await User.delete_groups(user_id=data.user_id,group_ids=data.group_ids)

    @staticmethod
    async def delete_users_from_group(request: Request, data: UsersToGroup):
        return await Group.delete_users(group_id=data.group_id, user_ids=data.user_ids)

