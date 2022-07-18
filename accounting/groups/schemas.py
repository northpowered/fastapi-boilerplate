from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union, List
import datetime



class GroupBase(BaseModel):
    
    name: Optional[str]
    active: Optional[bool] = True
    class Config:
        orm_mode = True

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