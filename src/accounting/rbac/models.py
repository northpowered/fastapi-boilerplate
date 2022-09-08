import datetime
from loguru import logger
from typing import TypeVar, Type, Tuple
from utils.piccolo import Table, uuid4_for_PK
from piccolo.columns import m2m
from piccolo.columns.column_types import (
    Text, Boolean, ForeignKey, LazyTableReference
)
from asyncpg.exceptions import UniqueViolationError
from utils.exceptions import IntegrityException, ObjectNotFoundException
from configuration import config
from piccolo.columns.readable import Readable
from accounting.users import User
from accounting.groups import Group
from accounting.roles import Role
from accounting.schemas import PermissionCreate

T_P = TypeVar('T_P', bound='Policy')
T_Pm = TypeVar('T_Pm', bound='Permission')

tz: datetime.timezone = config.Main.tz


class Permission(Table, tablename="permissions"):

    id = Text(primary_key=True, index=True, default=uuid4_for_PK)
    name = Text(unique=True, index=False, null=False)
    object = Text(unique=True, index=True, null=False)
    description = Text(unique=False, index=False, null=True)
    policies = m2m.M2M(LazyTableReference("Policy", module_path=__name__))

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])

    @classmethod
    async def get_all(cls: Type[T_Pm], offset: int, limit: int) -> list[T_Pm]:
        resp: list[T_Pm] = await cls.objects().limit(limit).offset(offset)
        for r in resp:
            await r.join_m2m()
        return resp

    @classmethod
    async def get_by_id(cls: Type[T_Pm], id: str) -> T_Pm:
        permission: T_Pm = await cls.objects().where(cls.id == id).first()
        try:
            assert permission
        except AssertionError:
            raise ObjectNotFoundException(object_name=__name__, object_id=id)
        else:
            await permission.join_m2m()
            return permission

    @classmethod
    async def add(cls: Type[T_Pm], name: str, object: str, description: str = str()) -> T_Pm:

        new_id = uuid4_for_PK()
        permission: T_Pm = cls(
            id=new_id,
            name=name,
            object=object,
            description=description
        )
        try:
            resp = await cls.insert(permission)
        except UniqueViolationError as ex:
            raise IntegrityException(ex)
        else:
            inserted_pk = resp[0].get('id')
            return await cls.get_by_id(inserted_pk)

    @classmethod
    async def add_from_list(cls: Type[T_Pm], objects: list[PermissionCreate]) -> Tuple[int, int]:
        existing_permissions: int = int()
        inserted_permissions: int = int()
        for permission in objects:
            permission.id = uuid4_for_PK()
            p: T_Pm = cls(
                **permission.dict()
            )
            try:
                await cls.insert(p)
            except UniqueViolationError:
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
    id = Text(primary_key=True, index=True, default=uuid4_for_PK)
    permission = ForeignKey(Permission, null=False)
    role = ForeignKey(Role, null=False)
    active = Boolean(nullable=False, default=True)
    name = Text(unique=False, index=False, null=False)
    description = Text(unique=False, index=False, null=True)

    @classmethod
    async def get_all(cls: Type[T_P], offset: int, limit: int) -> list[T_P]:
        # type: ignore
        resp: list[T_P] = await cls.objects(cls.all_related()).limit(limit).offset(offset)
        return resp

    @classmethod
    async def get_by_id(cls: Type[T_P], id: str) -> T_P:
        # type: ignore
        policy: T_P = await cls.objects(cls.all_related()).where(cls.id == id).first()
        try:
            assert policy
        except AssertionError:
            raise ObjectNotFoundException(object_name=__name__, object_id=id)
        else:
            return policy

    @classmethod
    async def add(
        cls: Type[T_P],
        permission_id: str,
        role_id: str,
        name: str | None = None,
        active: bool = True,
        description: str = str()
    ) -> T_P:
        permission: Permission = await Permission.get_by_id(id=permission_id)
        role: Role = await Role.get_by_id(id=role_id)
        new_id: str = uuid4_for_PK()
        if not name:
            name = f"{role.name}->{permission.object}"
        policy: T_P = cls(
            id=new_id,
            permission=permission,
            role=role,
            active=active,
            name=name,
            description=description
        )
        try:
            resp = await cls.insert(policy)
        except UniqueViolationError as ex:
            raise IntegrityException(ex)
        else:
            inserted_pk = resp[0].get('id')
            return await cls.get_by_id(inserted_pk)

    @classmethod
    async def update_by_id(cls: Type[T_P], id: str, data: dict) -> T_P:
        await cls.update(**data).where(cls.id == id)
        return await cls.get_by_id(id)

    @classmethod
    async def delete_by_id(cls: Type[T_P], id: str) -> None:
        await cls.get_by_id(id)
        await cls.delete().where(cls.id == id)
