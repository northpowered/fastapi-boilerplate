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