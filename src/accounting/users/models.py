from utils.piccolo import Table, uuid4_for_PK, get_pk_from_resp
from piccolo.columns.column_types import (
    Text, Boolean, Timestamp, LazyTableReference
)
from piccolo.columns import m2m
import datetime
from utils.crypto import create_password_hash
from typing import TypeVar, Type, Optional
from loguru import logger
from asyncpg.exceptions import UniqueViolationError, SyntaxOrAccessError
from utils.exceptions import IntegrityException, ObjectNotFoundException, BaseBadRequestException
from piccolo.columns.readable import Readable
from configuration import config

T_U = TypeVar('T_U', bound='User')


def foo() -> datetime.datetime:
    return datetime.datetime.now()


class User(Table, tablename="users"):

    # Main section
    id = Text(primary_key=True, index=True, default=uuid4_for_PK)
    username = Text(unique=True, index=True, null=False)
    email = Text(unique=True, index=False, nullable=True)
    password = Text(unique=False, index=False, null=False)

    first_name = Text(null=True)
    last_name = Text(null=True)
    # Flags
    active = Boolean(nullable=False, default=True)
    admin = Boolean(
        default=False, help_text="An admin can log into the Piccolo admin GUI."
    )
    superuser = Boolean(
        default=False,
        help_text=(
            "If True, this user can manage other users's passwords in the "
            "Piccolo admin GUI."
        ),
    )
    # Dates
    created_at = Timestamp(null=True)
    updated_at = Timestamp(null=True)
    last_login = Timestamp(null=True)
    birthdate = Timestamp(null=True)
    # Relations
    roles = m2m.M2M(LazyTableReference(
        "M2MUserRole", module_path='accounting'))
    groups = m2m.M2M(LazyTableReference(
        "M2MUserGroup", module_path='accounting'))

    def is_valid_password(self, plain_password) -> bool:
        return self.password == create_password_hash(plain_password)

    def is_active(self) -> bool:
        return self.active

    def get_user_id(self) -> str:
        return str(self.id)

    async def update_login_ts(self) -> None:
        data = {
            'last_login': datetime.datetime.now()
        }
        await self.update_by_id(
            self.id,
            data,
            update_ts=False
        )
        return None

    @classmethod
    async def add(cls: Type[T_U], username: str, password: str, email: str, as_superuser: bool = False) -> T_U:

        new_id = uuid4_for_PK()
        password_hash: str = create_password_hash(password)
        user: T_U = cls(
            id=new_id,
            username=username,
            password=password_hash,
            email=email,
            superuser=as_superuser,
            admin=as_superuser
        )
        try:
            resp = await cls.insert(user)
        except UniqueViolationError as ex:
            raise IntegrityException(ex)
        else:
            inserted_pk: str | None = get_pk_from_resp(resp, 'id')
            return await cls.get_by_id(inserted_pk)  # type: ignore

    @classmethod
    async def get_all(cls: Type[T_U], offset: int, limit: int) -> list[T_U]:
        resp: list[T_U] = await cls.objects().limit(limit).offset(offset)
        # Running JOIN for m2m relations, I don`t now how to do this shit better
        for r in resp:
            await r.join_m2m()
        return resp

    @classmethod
    async def get_by_id(cls: Type[T_U], id: str) -> T_U:
        user: T_U = await cls.objects().where(cls.id == id).first()
        try:
            assert user
        except AssertionError:
            raise ObjectNotFoundException(object_name=__name__, object_id=id)
        else:
            await user.join_m2m()
            return user

    @classmethod
    async def get_by_username(cls: Type[T_U], username: str, raise_404: bool = True) -> T_U | None:
        user: T_U = await cls.objects().where(cls.username == username).first()
        try:
            assert user
        except AssertionError:
            if raise_404:
                raise ObjectNotFoundException(
                    object_name=__name__, object_id=username)
            else:
                return None
        else:
            await user.join_m2m()
            return user

    @classmethod
    async def get_by_email(cls: Type[T_U], email: str, raise_404: bool = True) -> T_U | None:
        user: T_U = await cls.objects().where(cls.email == email).first()
        try:
            assert user
        except AssertionError:
            if raise_404:
                raise ObjectNotFoundException(
                    object_name=__name__, object_id=email)
            else:
                return None
        else:
            await user.join_m2m()
            return user

    @classmethod
    async def update_by_id(cls: Type[T_U], id: str, data: dict, update_ts: bool = True) -> T_U:
        if update_ts:
            data['updated_at'] = datetime.datetime.now()
        await cls.update(**data).where(cls.id == id)
        return await cls.get_by_id(id)

    @classmethod
    async def change_password(cls: Type[T_U], id: str, old_plaintext_password: str, new_plaintext_password: str) -> T_U:
        user: T_U = await cls.get_by_id(id)
        try:
            assert old_plaintext_password != new_plaintext_password, 'Passwords are equal'
            assert user.password == create_password_hash(
                old_plaintext_password), 'Invalid old password'
            data: dict = {
                'password': create_password_hash(new_plaintext_password)
            }
            return await cls.update_by_id(id, data)
        except AssertionError as ex:
            raise BaseBadRequestException(str(ex))

    @classmethod
    async def delete_by_id(cls: Type[T_U], id: str) -> None:
        await cls.get_by_id(id)
        await cls.delete().where(cls.id == id)

    @classmethod
    async def authenticate_user(cls: Type[T_U], username: str, password: str) -> T_U | None:
        user: T_U | None
        login_fields: list[str] = config.Security.available_login_fields
        # We are using searching in the list instead of raw attrs to avoid SQL injections
        for field in login_fields:
            try:
                match field:
                    case "username": user = await cls.get_by_username(username, raise_404=False)
                    case "email": user = await cls.get_by_email(username, raise_404=False)
                    case _: raise ObjectNotFoundException(object_name='User', object_id=username)
                # We set raise_404=False to avoid 404 Exception and try to find User with another field
                assert user
            except AssertionError:
                # Step forward to try another field
                continue
            else:
                # Break the loop, if the found user
                break
        try:
            # Check the result from last field
            assert user
        except AssertionError:
            raise ObjectNotFoundException(
                object_name='User', object_id=username)
        try:
            assert user.is_valid_password(
                plain_password=password), 'Bad credentials'  # type: ignore
            assert user.is_active(), 'User was deactivated'  # type: ignore
        except AssertionError as ex:
            logger.warning(f'AUTH | {ex} | {username}')
            raise BaseBadRequestException(str(ex))

        else:
            await user.update_login_ts()  # type: ignore
            logger.info(f'AUTH | SUCCESS | {username}')
            return user

    @classmethod
    async def login(cls, username: str, password: str) -> Optional[int]:
        """
        Implementation of 'login' method for piccolo admin (session auth)

        :returns:
            The id of the user if a match is found, otherwise ``None``.
        """
        user = await cls.authenticate_user(username, password)
        if not user:
            return None
        else:
            return user.id  # type: ignore

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.username])

    @classmethod
    async def add_roles(cls: Type[T_U], user_id: str, role_ids: list[str]):
        from accounting import Role  # CircularImport error
        user: T_U = await cls.objects().get(cls.id == user_id)
        for role_id in role_ids:
            role = await Role.get_by_id(role_id)
            await user.add_m2m(
                role,  # type: ignore
                m2m=cls.roles
            )
        return await cls.get_by_id(user_id)

    @classmethod
    async def delete_roles(cls: Type[T_U], user_id: str, role_ids: list[str]):
        from accounting import Role  # CircularImport error
        user: T_U = await cls.objects().get(cls.id == user_id)
        for role_id in role_ids:
            role = await Role.get_by_id(role_id)
            await user.remove_m2m(
                role,  # type: ignore
                m2m=cls.roles
            )
        return await cls.get_by_id(user_id)

    @classmethod
    async def add_groups(cls: Type[T_U], user_id: str, group_ids: list[str]):
        from accounting import Group  # CircularImport error
        user: T_U = await cls.objects().get(cls.id == user_id)
        for group_id in group_ids:
            group = await Group.get_by_id(group_id)
            await user.add_m2m(
                group,  # type: ignore
                m2m=cls.groups
            )
        return await cls.get_by_id(user_id)

    @classmethod
    async def delete_groups(cls: Type[T_U], user_id: str, group_ids: list[str]):
        from accounting import Group  # CircularImport error
        user: T_U = await cls.objects().get(cls.id == user_id)
        for group_id in group_ids:
            group = await Group.get_by_id(group_id)
            await user.remove_m2m(
                group,  # type: ignore
                m2m=cls.groups
            )
        return await cls.get_by_id(user_id)

    async def get_all_user_roles(self):
        from accounting import Role
        await self.join_m2m()
        roles: list[Role] = self.roles
        return roles
