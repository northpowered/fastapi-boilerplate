from fastapi import Request, Response
from accounting.schemas import (
    RolesToUser,
    UsersToRole,
    UsersToGroup,
    GroupesToUser,
    PolicyCreate,
    PolicyUpdate)
from accounting.users import User
from accounting.groups import Group
from accounting.roles import Role
from .models import Policy, Permission
from accounting.decorators import AAA_endpoint_oauth2


class UserRoleCRUD():

    @staticmethod
    @AAA_endpoint_oauth2()
    async def add_roles_to_user(request: Request, data: RolesToUser):
        return await User.add_roles(user_id=data.user_id, role_ids=data.role_ids)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def add_users_to_role(request: Request, data: UsersToRole):
        return await Role.add_users(role_id=data.role_id, user_ids=data.user_ids)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def delete_roles_from_user(request: Request, data: RolesToUser):
        return await User.delete_roles(user_id=data.user_id, role_ids=data.role_ids)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def delete_users_from_role(request: Request, data: UsersToRole):
        return await Role.delete_users(role_id=data.role_id, user_ids=data.user_ids)


class UserGroupCRUD():

    @staticmethod
    @AAA_endpoint_oauth2()
    async def add_groups_to_user(request: Request, data: GroupesToUser):
        return await User.add_groups(user_id=data.user_id, group_ids=data.group_ids)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def add_users_to_group(request: Request, data: UsersToGroup):
        return await Group.add_users(group_id=data.group_id, user_ids=data.user_ids)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def delete_groups_from_user(request: Request, data: GroupesToUser):
        return await User.delete_groups(user_id=data.user_id, group_ids=data.group_ids)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def delete_users_from_group(request: Request, data: UsersToGroup):
        return await Group.delete_users(group_id=data.group_id, user_ids=data.user_ids)


class PermissionCRUD():

    @staticmethod
    @AAA_endpoint_oauth2()
    async def get_all_permissions(request: Request, offset: int = 0, limit: int = 100):
        return await Permission.get_all(offset=offset, limit=limit)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def get_permission(request: Request, id: str):
        return await Permission.get_by_id(id=id)


class PolicyCRUD():

    @staticmethod
    @AAA_endpoint_oauth2()
    async def get_all_policies(request: Request, offset: int = 0, limit: int = 100):
        """
        ### READ list[Policy] with offset and limit
        #### Args:\n
            offset (int, optional): Defaults to 0.\n
            limit (int, optional): Defaults to 100.\n
        #### Returns:
            list[Policy]
        """
        return await Policy.get_all(offset=offset, limit=limit)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def get_policy(id: str):
        """
        ### READ one {Policy} by id
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
            Policy | None
        """
        return await Policy.get_by_id(id)

    @staticmethod
    @AAA_endpoint_oauth2()
    async def add_policy(request: Request, data: PolicyCreate):
        return await Policy.add(**data.dict(exclude_unset=True))

    @staticmethod
    @AAA_endpoint_oauth2()
    async def update_policy(id: str, policy: PolicyUpdate):
        """
        ### Update one policy (full or partial)
        Args:\n
            policy (Policy): {
                name: str (Unique)
                price: int
            }
        Returns:
            Policy
        """
        return await Policy.update_by_id(id=id, data=policy.dict(exclude_unset=True))

    @staticmethod
    @AAA_endpoint_oauth2()
    async def delete_policy(id: str):
        """
        ### DELETE one policy by ID
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
        None, code=204
        """
        await Policy.delete_by_id(id)
        return Response(status_code=204)
