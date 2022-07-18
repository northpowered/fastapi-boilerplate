from piccolo.table import Table
from piccolo.columns.column_types import (
    Text, Boolean, Timestamp, ForeignKey,
    LazyTableReference
)
from piccolo.columns import Timestamp, m2m
from uuid import uuid4
import datetime
from utils.crypto import create_password_hash
from typing import TypeVar, Type, Optional
from loguru import logger
from asyncpg.exceptions import UniqueViolationError
from utils.exceptions import IntegrityException, ObjectNotFoundException, BaseBadRequestException
from piccolo.columns.readable import Readable


T_U = TypeVar('T_U', bound='User')

class User(Table, tablename="users"):

    # Main section
    id = Text(primary_key=True, index=True)
    username = Text(unique=True, index=True, null=False)
    email = Text(unique=False, index=False, nullable=True)
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
    created_at = Timestamp(nullable=False,
                        default=datetime.datetime.now())
    updated_at = Timestamp(nullable=False,
                        default=datetime.datetime.now())
    last_login = Timestamp(nullable=True)
    birthdate = Timestamp(nullable=True)
    #Relations
    roles = m2m.M2M(LazyTableReference("M2MUserRole", module_path='accounting'))
    groups = m2m.M2M(LazyTableReference("M2MUserGroup", module_path='accounting'))

    def is_valid_password(self, plain_password) -> bool:
        return self.password == create_password_hash(plain_password)

    def is_active(self) -> bool:
        return self.active

    def get_user_id(self):
        return str(self.id)

    async def update_login_ts(self)->None:
        data = {
            'last_login':datetime.datetime.now()
        }
        await self.update_by_id(
            self.id,
            data,
            update_ts=False
        )
        return None

    @classmethod
    async def add(cls: Type[T_U], username: str, password: str, email: str)->Type[T_U]:

        new_id = str(uuid4())
        password_hash: str = create_password_hash(password)
        user: T_U = cls(
            id = new_id,
            username = username,
            password = password_hash,
            email = email
        )
        try:
            resp = await cls.insert(user)
        except UniqueViolationError as ex:
            raise IntegrityException(ex)
        else:
            inserted_pk = resp[0].get('id')
            return await cls.get_by_id(inserted_pk)

    @classmethod
    async def get_all(cls: Type[T_U], offset: int, limit: int)->list[Type[T_U]]:
        return await cls.objects().limit(limit).offset(offset)

    @classmethod
    async def get_by_id(cls: Type[T_U], id: str)->Type[T_U]:
        user: Type[T_U] = await cls.objects().where(cls.id == id).first()
        try:
            assert user
        except AssertionError as ex:
            raise ObjectNotFoundException(object_name=__name__,object_id=id)
        else:
            return user

    @classmethod
    async def get_by_username(cls: Type[T_U], username: str)->Type[T_U]:
        user: Type[T_U] = await cls.objects().where(cls.username == username).first()
        try:
            assert user
        except AssertionError as ex:
            raise ObjectNotFoundException(object_name=__name__,object_id=username)
        else:
            return user

    @classmethod
    async def update_by_id(cls: Type[T_U],id: str, data: dict, update_ts: bool=True)->Type[T_U]:
        if update_ts:
            data['updated_at'] = datetime.datetime.now()
        await cls.update(**data).where(cls.id == id)
        return await cls.get_by_id(id)

    @classmethod
    async def change_password(cls: Type[T_U], id: str, old_plaintext_password: str, new_plaintext_password: str)->Type[T_U]:
        user: Type[T_U] = await cls.get_by_id(id)
        try:
            assert old_plaintext_password != new_plaintext_password, 'Passwords are equal'
            assert user.password == create_password_hash(old_plaintext_password), 'Invalid old password'
            data: dict = {
                'password':create_password_hash(new_plaintext_password)
            }
            return await cls.update_by_id(id, data)
        except AssertionError as ex:
            raise BaseBadRequestException(str(ex))
        
    @classmethod
    async def delete_by_id(cls: Type[T_U], id: str)->None:
        await cls.get_by_id(id)
        await cls.delete().where(cls.id == id)

    @classmethod
    async def authenticate_user(cls: Type[T_U], username: str, password: str)->Type[T_U]:
        user: Type[T_U] = await cls.get_by_username(username)
        try:
            assert user.is_valid_password(plain_password=password),'Bad credentials' # type: ignore
            assert user.is_active(), 'User was deactivated' # type: ignore
        except AssertionError as ex:
            logger.warning(f'AUTH | {ex} | {username}')
            raise BaseBadRequestException(str(ex))
            
        else:
            await user.update_login_ts() # type: ignore
            return user

    @classmethod
    async def login(cls, username: str, password: str)->Optional[int]:
        """
        Implementation of 'login' method for piccolo admin (session auth)

        :returns:
            The id of the user if a match is found, otherwise ``None``.
        """
        user = await cls.authenticate_user(username,password)
        if not user:
            return None
        else:
            return user.id # type: ignore

    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.username])