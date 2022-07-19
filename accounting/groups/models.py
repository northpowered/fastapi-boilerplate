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

T_G = TypeVar('T_G', bound='Group')

class Group(Table, tablename="groups"):

    id = Text(primary_key=True, index=True, default=str(uuid4()))
    name = Text(unique=True, index=True, null=False)
    active = Boolean(nullable=False, default=True)
    users = m2m.M2M(LazyTableReference("M2MUserGroup", module_path='accounting'))

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

