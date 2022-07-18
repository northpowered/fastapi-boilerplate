from loguru import logger
from .models import User, Role, Group
from .schemas import (
    UserUpdate,
    UserCreate,
    UserPasswordChange,
    RoleCreate,
    RoleUpdate,
    GroupCreate,
    GroupUpdate
)
from fastapi import Request, Response

class UserCRUD():
    
    @staticmethod
    async def get_all_users(request: Request, offset: int = 0, limit: int = 100):
        """
        ### READ list[User] with offset and limit
        #### Args:\n
            offset (int, optional): Defaults to 0.\n
            limit (int, optional): Defaults to 100.\n
        #### Returns:
            list[User]
        """
        return await User.get_all(offset=offset,limit=limit)
    @staticmethod
    async def get_user(id: str):
        """
        ### READ one {User} by id
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
            User | None
        """
        return await User.get_by_id(id)
    @staticmethod
    async def create_user(user: UserCreate):
        """
        ### CREATE user
        #### Args:\n
            user (User): {
                username: str (Unique)
                password: str
                email: str
                active: bool
            }
        #### Returns:
            User
        """

        return await User.add(**user.dict())
    @staticmethod
    async def update_user(id: str, user: UserUpdate):
        """
        ### Update one user (full or partial)
        Args:\n
            user (User): {
                name: str (Unique)
                price: int
            }
        Returns:
            User
        """
        return await User.update_by_id(id = id, data = user.dict())
    @staticmethod
    async def patch_user(id: str, user: UserPasswordChange):
        """
        ### User password change
        Args:\n
            PasswordChange (UserPasswordChange): {
                old_password: Optional[str | None] #Admin can change password without old_password
                new_password: str
            }
        Returns:
            User
        """
        return await User.change_password(
            id=id, 
            old_plaintext_password=user.old_password, 
            new_plaintext_password=user.new_password
        )
    @staticmethod
    async def delete_user(id: str):
        """
        ### DELETE one user by ID
        #### Args:\n
            id (str): UUID4 PK
        #### Returns:
        None, code=204
        """
        await User.delete_by_id(id)
        return Response(status_code=204)

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

