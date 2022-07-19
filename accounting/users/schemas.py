from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union, List
import datetime
from accounting.roles.schemas import RoleBase
from accounting.groups.schemas import GroupBase
class UserBase(BaseModel):
    
    username: Optional[str]
    email: Optional[EmailStr]
    active: Optional[bool] = True
    birthdate: Optional[datetime.datetime | None]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    last_login: Optional[datetime.datetime | None]

    class Config:
        orm_mode = True

class UserRead(UserBase):
    """
    READ model for USER subject
    """
    id: Optional[str]
    roles: list[RoleBase]
    groups: list[GroupBase]

class UserUpdate(UserBase):
    pass

class UserCreate(BaseModel):
    """
    CREATE model for USER subject with required fields
    """
    username: str
    password: str
    email: EmailStr

class UserPasswordChange(BaseModel):
    #TODO Admin can change password without old_password
    old_password: str
    new_password: str

    class Config:
        orm_mode = True
