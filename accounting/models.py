from uuid import uuid4
import datetime
from loguru import logger

from typing import TypeVar, Type, Optional
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

T_R = TypeVar('T_R', bound='Role')
T_G = TypeVar('T_G', bound='Group')
T_P = TypeVar('T_P', bound='Policy')
T_Pm = TypeVar('T_Pm', bound='Permission')

tz: datetime.timezone = config.main.tz

class Role(Table, tablename="roles"):

    id = Text(primary_key=True, index=True)
    name = Text(unique=True, index=True, null=False)
    active = Boolean(nullable=False, default=True)
    users = m2m.M2M(LazyTableReference("M2MUserRole", module_path=__name__))
    policies = m2m.M2M(LazyTableReference("Policy", module_path=__name__))

    @classmethod
    async def get_all(cls: Type[T_R], offset: int, limit: int)->list[Type[T_R]]:
        return await cls.objects().limit(limit).offset(offset)

    @classmethod
    async def get_by_id(cls: Type[T_R], id: str)->Type[T_R]:
        role: Type[T_R] = await cls.objects().where(cls.id == id).first()
        try:
            assert role
        except AssertionError as ex:
            raise ObjectNotFoundException(object_name=__name__,object_id=id)
        else:
            return role

    @classmethod
    async def get_by_name(cls: Type[T_R], name: str)->Type[T_R]:
        role: Type[T_R] = await cls.objects().where(cls.name == name).first()
        try:
            assert role
        except AssertionError as ex:
            raise ObjectNotFoundException(object_name=__name__,object_id=name)
        else:
            return role

    @classmethod
    async def add(cls: Type[T_R], name: str, active: bool)->Type[T_R]:

        new_id = str(uuid4())
        role: T_R = cls(
            id = new_id,
            name = name,
            active = active
        )
        try:
            resp = await cls.insert(role)
        except UniqueViolationError as ex:
            raise IntegrityException(ex)
        else:
            inserted_pk = resp[0].get('id')
            return await cls.get_by_id(inserted_pk)

    @classmethod
    async def update_by_id(cls: Type[T_R],id: str, data: dict)->Type[T_R]:
        await cls.update(**data).where(cls.id == id)
        return await cls.get_by_id(id)

    @classmethod
    async def delete_by_id(cls: Type[T_R], id: str)->None:
        await cls.get_by_id(id)
        await cls.delete().where(cls.id == id)


class Group(Table, tablename="groups"):

    id = Text(primary_key=True, index=True)
    name = Text(unique=True, index=True, null=False)
    active = Boolean(nullable=False, default=True)
    users = m2m.M2M(LazyTableReference("M2MUserGroup", module_path=__name__))

    @classmethod
    async def get_all(cls: Type[T_G], offset: int, limit: int)->list[Type[T_G]]:
        return await cls.objects().limit(limit).offset(offset)

    @classmethod
    async def get_by_id(cls: Type[T_G], id: str)->Type[T_G]:
        group: Type[T_G] = await cls.objects().where(cls.id == id).first()
        try:
            assert group
        except AssertionError as ex:
            raise ObjectNotFoundException(object_name=__name__,object_id=id)
        else:
            return group

    @classmethod
    async def get_by_name(cls: Type[T_G], name: str)->Type[T_G]:
        group: Type[T_G] = await cls.objects().where(cls.name == name).first()
        try:
            assert group
        except AssertionError as ex:
            raise ObjectNotFoundException(object_name=__name__,object_id=name)
        else:
            return group

    @classmethod
    async def add(cls: Type[T_G], name: str, active: bool)->Type[T_G]:

        new_id = str(uuid4())
        group: T_G = cls(
            id = new_id,
            name = name,
            active = active
        )
        try:
            resp = await cls.insert(group)
        except UniqueViolationError as ex:
            raise IntegrityException(ex)
        else:
            inserted_pk = resp[0].get('id')
            return await cls.get_by_id(inserted_pk)

    @classmethod
    async def update_by_id(cls: Type[T_G],id: str, data: dict)->Type[T_G]:
        await cls.update(**data).where(cls.id == id)
        return await cls.get_by_id(id)

    @classmethod
    async def delete_by_id(cls: Type[T_G], id: str)->None:
        await cls.get_by_id(id)
        await cls.delete().where(cls.id == id)


class Permission(Table, tablename="permissions"):

    id = Text(primary_key=True, index=True)
    name = Text(unique=True, index=False, null=False)
    object = Text(unique=True, index=True, null=False)
    description = Text(unique=False, index=False, null=True)
    policies = m2m.M2M(LazyTableReference("Policy", module_path=__name__))


class M2MUserRole(Table):
    user = ForeignKey(User)
    role = ForeignKey(Role)

class M2MUserGroup(Table):
    user = ForeignKey(User)
    group = ForeignKey(Group)

class Policy(Table, tablename="policies"):
    id = Text(primary_key=True, index=True)
    permission = ForeignKey(Permission)
    role = ForeignKey(Role)