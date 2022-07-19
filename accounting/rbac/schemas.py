from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union, List
import datetime


class PermissionBase(BaseModel):
    
    name: str
    object: str
    description: Optional[str]

    class Config:
        orm_mode = True


class PermissionCreate(PermissionBase):
    id: Optional[str]

class RolesToUser(BaseModel):
    user_id: str
    role_ids: list[str]

class RoleToUser(BaseModel):
    user_id: str
    role_ids: str

class UsersToRole(BaseModel):
    role_id: str
    user_ids: list[str]
