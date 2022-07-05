from uuid import uuid4
import datetime
import secrets
from loguru import logger
from utils.crypto import create_password_hash
from typing import TypeVar, Type, Optional, cast
from piccolo.table import Table
from piccolo.columns import Timestamp
from piccolo.columns.defaults.timestamp import TimestampOffset
from piccolo.columns.column_types import Text, Boolean, Timestamp, Timestamptz
from piccolo_api.session_auth.tables import SessionsBase
from asyncpg.exceptions import UniqueViolationError
from utils.exceptions import IntegrityException, ObjectNotFoundException, BaseBadRequestException
from piccolo.utils.sync import run_sync
from configuration import config

T_U = TypeVar('T_U', bound='User')
T_S = TypeVar('T_S', bound='Sessions')

tz: datetime.timezone = config.main.tz
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
            raise BaseBadRequestException(ex)
        
    @classmethod
    async def delete_by_id(cls: Type[T_U], id: str)->None:
        await cls.get_by_id(id)
        await cls.delete().where(cls.id == id)

    @classmethod
    async def authenticate_user(cls: Type[T_U], username: str, password: str)->Type[T_U]:
        user = await cls.get_by_username(username)
        try:
            assert user.is_valid_password(password),'Bad credentials'
            assert user.is_active(), 'User was deactivated'
        except AssertionError as ex:
            logger.warning(f'AUTH | {ex} | {username}')
            raise BaseBadRequestException(ex)
            
        else:
            await user.update_login_ts()
            return user


    #
    @classmethod
    async def login(cls, username: str, password: str) -> Optional[int]:
        """
        Implementation of 'login' method for piccolo admin (session auth)

        :returns:
            The id of the user if a match is found, otherwise ``None``.
        """
        user = await cls.authenticate_user(username,password)
        if not user:
            return None
        else:
            return user.id

class Sessions(SessionsBase, tablename="sessions"):
    """
    INHERITED from SessionsBase
    Use this table, or inherit from it, to create for a session store.

    We set a hard limit on the expiry date - it can keep on getting extended
    up until this value, after which it's best to invalidate it, and either
    require login again, or just create a new session token.
    """

    token = Text(length=100, null=False)
    user_id = Text(null=False)
    expiry_date: Timestamp | datetime.datetime = Timestamp(
        default=TimestampOffset(hours=1), null=False
    )
    max_expiry_date: Timestamp | datetime.datetime = Timestamp(
        default=TimestampOffset(days=7), null=False
    )

    @classmethod
    async def create_session(
        cls: Type[T_S],
        user_id: str,
        expiry_date: Optional[datetime.datetime] = None,
        max_expiry_date: Optional[datetime.datetime] = None,
    ) -> Type[T_S]:
        while True:
            token = secrets.token_urlsafe(nbytes=32)
            if not await cls.exists().where(cls.token == token).run():
                break

        session = cls(token=token, user_id=user_id)
        if expiry_date:
            session.expiry_date = expiry_date
        if max_expiry_date:
            session.max_expiry_date = max_expiry_date

        await session.save().run()

        return session

    @classmethod
    def create_session_sync(
        cls, user_id: str, expiry_date: Optional[datetime.datetime] = None
    ) -> Type[T_S]:
        return run_sync(cls.create_session(user_id, expiry_date))

    @classmethod
    async def get_user_id(
        cls, token: str, increase_expiry: Optional[datetime.timedelta] = None
    ) -> Optional[str]:
        """
        Returns the user_id if the given token is valid, otherwise None.

        :param increase_expiry:
            If set, the `expiry_date` will be increased by the given amount
            if it's close to expiring. If it has already expired, nothing
            happens. The `max_expiry_date` remains the same, so there's a hard
            limit on how long a session can be used for.
        """
        session: Type[T_S] = (
            await cls.objects().where(cls.token == token).first().run()
        )

        if not session:
            return None

        now = datetime.datetime.now()
        if (session.expiry_date > now) and (session.max_expiry_date > now):
            if increase_expiry and (
                cast(datetime.datetime, session.expiry_date) - now < increase_expiry
            ):
                session.expiry_date = (
                    cast(datetime.datetime, session.expiry_date) + increase_expiry
                )
                await session.save().run()

            return cast(Optional[str], session.user_id)
        else:
            return None

    @classmethod
    def get_user_id_sync(cls, token: str) -> Optional[str]:
        return run_sync(cls.get_user_id(token))

    @classmethod
    async def remove_session(cls, token: str):
        await cls.delete().where(cls.token == token).run()

    @classmethod
    def remove_session_sync(cls, token: str):
        return run_sync(cls.remove_session(token))


            