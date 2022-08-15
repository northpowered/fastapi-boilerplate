from loguru import logger
from typing import TypeVar, Type
from utils.piccolo import Table, uuid4_for_PK, get_pk_from_resp
from piccolo.columns import m2m
from piccolo.columns.column_types import (
    Text, Boolean, LazyTableReference
)
from piccolo.columns.readable import Readable
from asyncpg.exceptions import UniqueViolationError
from utils.exceptions import IntegrityException, ObjectNotFoundException, BaseBadRequestException

T_R = TypeVar('T_R', bound='Role')

class Role(Table, tablename="roles"):

    id = Text(primary_key=True, index=True, default=uuid4_for_PK)
    name = Text(unique=True, index=True, null=False)
    active = Boolean(nullable=False, default=True)
    users = m2m.M2M(LazyTableReference("M2MUserRole", module_path='accounting'))
    policies = m2m.M2M(LazyTableReference("Policy", module_path='accounting'))

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])

    @classmethod
    async def get_all(cls: Type[T_R], offset: int, limit: int)->list[T_R]:
        resp: list[T_R] = await cls.objects().limit(limit).offset(offset)
        for r in resp:
            await r.join_m2m()
        return resp

    @classmethod
    async def get_by_id(cls: Type[T_R], id: str)->T_R:
        role: T_R = await cls.objects().where(cls.id == id).first()
        try:
            assert role
        except AssertionError as ex:
            raise ObjectNotFoundException(object_name=__name__,object_id=id)
        else:
            await role.join_m2m()
            return role

    @classmethod
    async def get_by_name(cls: Type[T_R], name: str)->T_R:
        role: T_R = await cls.objects().where(cls.name == name).first()
        try:
            assert role
        except AssertionError as ex:
            raise ObjectNotFoundException(object_name=__name__,object_id=name)
        else:
            await role.join_m2m()
            return role

    @classmethod
    async def add(cls: Type[T_R], name: str, active: bool)->T_R:

        new_id: str = uuid4_for_PK()
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
            inserted_pk = get_pk_from_resp(resp,'id')
            return await cls.get_by_id(inserted_pk) #type: ignore

    @classmethod
    async def update_by_id(cls: Type[T_R],id: str, data: dict)->T_R:
        await cls.update(**data).where(cls.id == id)
        return await cls.get_by_id(id)

    @classmethod
    async def delete_by_id(cls: Type[T_R], id: str)->None:
        await cls.get_by_id(id)
        await cls.delete().where(cls.id == id)

    @classmethod
    async def add_users(cls: Type[T_R], role_id: str, user_ids: list[str]):
        from accounting import User #CircularImport error
        role: T_R = await cls.objects().get(cls.id==role_id)
        for user_id in user_ids:
            user = await User.get_by_id(user_id)
            await role.add_m2m(
                user, # type: ignore
                m2m=cls.users
            )
        return await cls.get_by_id(role_id)
    
    @classmethod
    async def delete_users(cls: Type[T_R], role_id: str, user_ids: list[str]):
        from accounting import User #CircularImport error
        role: T_R = await cls.objects().get(cls.id==role_id)
        for user_id in user_ids:
            user = await User.get_by_id(user_id)
            await role.remove_m2m(
                user, # type: ignore
                m2m=cls.users
            )
        return await cls.get_by_id(role_id)