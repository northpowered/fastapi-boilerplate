from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

""" Base pydantic models """


class UserBase(BaseModel):
    """User schema without joined fields"""
    id: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    active: Optional[bool] = True
    birthdate: Optional[datetime.datetime | None]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    last_login: Optional[datetime.datetime | None]

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    """Role schema without joined fields"""
    id: Optional[str]
    name: Optional[str]
    active: Optional[bool] = True

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    """Group schema without joined fields"""
    name: Optional[str]
    active: Optional[bool] = True

    class Config:
        orm_mode = True


class PermissionBase(BaseModel):
    """Permission schema without joined fields"""
    name: str
    object: str
    description: Optional[str]

    class Config:
        orm_mode = True


class PolicyBase(BaseModel):
    """Policy schema without joined fields"""
    id: Optional[str]
    name: Optional[str]
    active: Optional[bool]
    description: Optional[str]

    class Config:
        orm_mode = True


""" CRUD pydantic models """


class UserRead(UserBase):
    """
    READ model for USER subject, with M2M fields
    """
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
    # TODO Admin can change password without old_password
    old_password: str
    new_password: str

    class Config:
        orm_mode = True


class RoleRead(RoleBase):
    """
    READ model for ROLE subject
    """
    users: list[UserBase]


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


class PermissionCreate(PermissionBase):
    id: Optional[str]


class RolesToUser(BaseModel):
    user_id: str
    role_ids: list[str]


class UsersToRole(BaseModel):
    role_id: str
    user_ids: list[str]


class GroupesToUser(BaseModel):
    user_id: str
    group_ids: list[str]


class UsersToGroup(BaseModel):
    group_id: str
    user_ids: list[str]


class PermissionRead(PermissionBase):
    policies: list[PolicyBase]


class PolicyRead(PolicyBase):
    permission: PermissionBase
    role: RoleBase


class PolicyCreate(BaseModel):
    permission_id: str
    role_id: str
    name: Optional[str]
    description: Optional[str]
    active: bool = True


class PolicyUpdate(PolicyBase):
    pass
