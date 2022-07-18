from fastapi.security import OAuth2PasswordRequestForm
from users import User
from .jwt import create_access_token, get_user_by_token
from fastapi import Depends

async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.authenticate_user(form_data.username,form_data.password)
    access_token = create_access_token(
        data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(current_user: User = Depends(get_user_by_token)):
    return current_user