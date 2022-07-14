from loguru import logger
from .models import User
from .schemas import (
    UserBase,
    UserRead,
    UserUpdate,
    UserCreate,
    UserPasswordChange
)
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from .auth import create_access_token, get_user_by_token

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


async def get_user(id: str):
    """
    ### READ one {User} by id
    #### Args:\n
        id (str): UUID4 PK
    #### Returns:
        User | None
    """
    return await User.get_by_id(id)

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


async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.authenticate_user(form_data.username,form_data.password)
    access_token = create_access_token(
        data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(current_user: User = Depends(get_user_by_token)):
    return current_user