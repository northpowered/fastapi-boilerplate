from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union, List
import datetime


class RoleBase(BaseModel):
    
    name: Optional[str]
    active: Optional[bool] = True
    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    
    name: Optional[str]
    active: Optional[bool] = True
    class Config:
        orm_mode = True


class PermissionBase(BaseModel):
    
    name: str
    object: str
    description: Optional[str]

    class Config:
        orm_mode = True

class RoleRead(RoleBase):
    """
    READ model for ROLE subject
    """
    id: str

class RoleCreate(BaseModel):
    """
    CREATE model for USER subject with required fields
    """
    name: str
    active: bool = True

class RoleUpdate(RoleBase):
    pass

class GroupRead(GroupBase):
    """
    READ model for GROUP subject
    """
    id: str

class GroupCreate(BaseModel):
    """
    CREATE model for GROUP subject with required fields
    """
    name: str
    active: bool = True

class GroupUpdate(GroupBase):
    pass