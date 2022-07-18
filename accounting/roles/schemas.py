from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union, List
import datetime

class RoleBase(BaseModel):
    
    name: Optional[str]
    active: Optional[bool] = True
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
