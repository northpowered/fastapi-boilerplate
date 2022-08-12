from loguru import logger
from .models import User
from accounting.schemas import (
    UserUpdate,
    UserCreate,
    UserPasswordChange
)
from fastapi import Request, Response
from accounting.decorators import AAA_endpoint_oauth2
class UserCRUD():
    
    @staticmethod
    @AAA_endpoint_oauth2()
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
    @AAA_endpoint_oauth2()
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
    @AAA_endpoint_oauth2()
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
    @AAA_endpoint_oauth2()
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
    @AAA_endpoint_oauth2()
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
    @AAA_endpoint_oauth2()
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
