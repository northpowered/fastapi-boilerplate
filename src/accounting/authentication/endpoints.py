from fastapi.security import OAuth2PasswordRequestForm
from accounting.users import User
from .jwt import create_access_token, get_user_by_token
from fastapi import Depends

async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Base auth endpoint with OAuth2PasswordBearer form
    for obtaining JWT

    Args:\n
        username: str - required
        password: str - required
        grant_type: str
        scope: str
        client_id: str
        client_secret: str


    Returns:\n
        access_token: str
        token_type: str
    """
    user = await User.authenticate_user(form_data.username,form_data.password)
    access_token = create_access_token(
        data={"sub": user.username}) # type: ignore
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(current_user: User = Depends(get_user_by_token)):
    """
    Obtaining {USER} object of authenticated user

    Returns:
        {USER}, see accounting.users
    """
    return current_user