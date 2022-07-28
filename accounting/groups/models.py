from uuid import uuid4
import datetime
import uuid
from loguru import logger
from typing import TypeVar, Type, Optional
from utils.piccolo import Table
from piccolo.columns import Timestamp, m2m
from piccolo.columns.column_types import (
    Text, Boolean, Timestamp, ForeignKey,
    LazyTableReference, UUID, PrimaryKey
)
from piccolo.columns.defaults.uuid import UUID4
from piccolo.columns.readable import Readable
from asyncpg.exceptions import UniqueViolationError
from utils.exceptions import IntegrityException, ObjectNotFoundException, BaseBadRequestException

T_G = TypeVar('T_G', bound='Group')

def gen_pk():
    yield str(uuid4())
print(next(gen_pk()))
print(next(gen_pk()))
print(next(gen_pk()))
print(next(gen_pk()))
class Group(Table, tablename="groups"):

    id = Text(primary_key=True, index=True, default=next(gen_pk()))
    name = Text(unique=True, index=True, null=False)
    active = Boolean(nullable=False, default=True)
    users = m2m.M2M(LazyTableReference("M2MUserGroup", module_path='accounting'))

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])

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

    @classmethod
    async def add_users(cls: Type[T_G], group_id: str, user_ids: list[str]):
        from accounting import User #CircularImport error
        group: T_G = await cls.objects().get(cls.id==group_id)
        for user_id in user_ids:
            user = await User.get_by_id(user_id)
            await group.add_m2m(
                user, # type: ignore
                m2m=cls.users
            )
        return await cls.get_by_id(group_id)
    
    @classmethod
    async def delete_users(cls: Type[T_G], group_id: str, user_ids: list[str]):
        from accounting import User #CircularImport error
        group: T_G = await cls.objects().get(cls.id==group_id)
        for user_id in user_ids:
            user = await User.get_by_id(user_id)
            await group.remove_m2m(
                user, # type: ignore
                m2m=cls.users
            )
        return await cls.get_by_id(group_id)