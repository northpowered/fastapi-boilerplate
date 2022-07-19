from uuid import uuid4
import datetime
from loguru import logger
from typing import TypeVar, Type, Optional, Tuple
from piccolo.table import Table
from piccolo.columns import Timestamp, m2m
from piccolo.columns.column_types import (
    Text, Boolean, Timestamp, ForeignKey,
    LazyTableReference
)
from asyncpg.exceptions import UniqueViolationError
from utils.exceptions import IntegrityException, ObjectNotFoundException, BaseBadRequestException
from configuration import config
from piccolo.columns.readable import Readable
from accounting import User, Role, Group
from .schemas import PermissionCreate

T_P = TypeVar('T_P', bound='Policy')
T_Pm = TypeVar('T_Pm', bound='Permission')

tz: datetime.timezone = config.main.tz

class Permission(Table, tablename="permissions"):

    id = Text(primary_key=True, index=True, default=str(uuid4()))
    name = Text(unique=True, index=False, null=False)
    object = Text(unique=True, index=True, null=False)
    description = Text(unique=False, index=False, null=True)
    policies = m2m.M2M(LazyTableReference("Policy", module_path=__name__))


    @classmethod
    async def get_by_id(cls: Type[T_Pm], id: str)->Type[T_Pm]:
        permission: Type[T_Pm] = await cls.objects().where(cls.id == id).first()
        try:
            assert permission
        except AssertionError as ex:
            raise ObjectNotFoundException(object_name=__name__,object_id=id)
        else:
            return permission

    @classmethod
    async def add(cls: Type[T_Pm], name: str, object: str, description: str = str())->Type[T_Pm]:

        new_id = str(uuid4())
        permission: T_Pm = cls(
            id = new_id,
            name = name,
            object = object,
            description = description
        )
        try:
            resp = await cls.insert(permission)
        except UniqueViolationError as ex:
            raise IntegrityException(ex)
        else:
            inserted_pk = resp[0].get('id')
            return await cls.get_by_id(inserted_pk)

    @classmethod
    async def add_from_list(cls: Type[T_Pm], objects: list[PermissionCreate])->Tuple[int,int]:
        existing_permissions: int = int()
        inserted_permissions: int = int()
        for permission in objects:
            permission.id = str(uuid4())
            p: T_Pm = cls(
                    **permission.dict()
            )  
            try:
                resp = await cls.insert(p)
            except UniqueViolationError as ex:
                existing_permissions = existing_permissions + 1
            else:
                inserted_permissions = inserted_permissions + 1
        return (existing_permissions, inserted_permissions)


class M2MUserRole(Table):
    user = ForeignKey(User)
    role = ForeignKey(Role)

class M2MUserGroup(Table):
    user = ForeignKey(User)
    group = ForeignKey(Group)

class Policy(Table, tablename="policies"):
    id = Text(primary_key=True, index=True, default=str(uuid4()))
    permission = ForeignKey(Permission)
    role = ForeignKey(Role)