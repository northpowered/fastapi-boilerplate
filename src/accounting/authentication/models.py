import datetime
import secrets
from loguru import logger
from typing import TypeVar, Type, Optional, cast
from piccolo.columns import Timestamp
from piccolo.columns.defaults.timestamp import TimestampOffset
from piccolo.columns.column_types import Text, Boolean, Timestamp, Timestamptz
from piccolo_api.session_auth.tables import SessionsBase
from asyncpg.exceptions import UniqueViolationError
from utils.exceptions import IntegrityException, ObjectNotFoundException, BaseBadRequestException
from piccolo.utils.sync import run_sync
from configuration import config
from accounting.users import T_U

T_S = TypeVar('T_S', bound='Sessions')

class Sessions(SessionsBase, tablename="sessions"):
    """
    INHERITED from SessionsBase
    Use this table, or inherit from it, to create for a session store.

    We set a hard limit on the expiry date - it can keep on getting extended
    up until this value, after which it's best to invalidate it, and either
    require login again, or just create a new session token.
    """

    token = Text(length=100, null=False) # type: ignore
    user_id = Text(null=False) # type: ignore
    expiry_date: Timestamp | datetime.datetime = Timestamp(
        default=TimestampOffset(hours=1), null=False
    )
    max_expiry_date: Timestamp | datetime.datetime = Timestamp(
        default=TimestampOffset(days=7), null=False
    )

    @classmethod
    async def create_session( # type: ignore
        cls: Type[T_S],
        user_id: str,
        expiry_date: Optional[datetime.datetime] = None,
        max_expiry_date: Optional[datetime.datetime] = None,
    ) -> Type[T_S]:
        while True:
            token: str = secrets.token_urlsafe(nbytes=32)
            if not await cls.exists().where(cls.token == token).run(): # type: ignore
                break

        session = cls(token=token, user_id=user_id)
        if expiry_date:
            session.expiry_date = expiry_date
        if max_expiry_date:
            session.max_expiry_date = max_expiry_date

        await session.save().run()
        return session # type: ignore

    @classmethod
    def create_session_sync( # type: ignore
        cls, user_id: str, expiry_date: Optional[datetime.datetime] = None
    ) -> Type[T_S]:
        return run_sync(cls.create_session(user_id, expiry_date))

    @classmethod
    async def get_user_id( # type: ignore
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
        session: Type[T_S] = ( # type: ignore
            await cls.objects().where(cls.token == token).first().run() # type: ignore
        )
        if not session:
            return None
        now = datetime.datetime.now()
        if (session.expiry_date > now) and (session.max_expiry_date > now): # type: ignore
            if increase_expiry and (
                cast(datetime.datetime, session.expiry_date) - now < increase_expiry # type: ignore
            ):
                session.expiry_date = ( # type: ignore
                    cast(datetime.datetime, session.expiry_date) + increase_expiry # type: ignore
                )
                await session.save().run() # type: ignore

            return cast(Optional[str], session.user_id) # type: ignore
        else:
            return None

    @classmethod
    def get_user_id_sync(cls, token: str) -> Optional[str]: # type: ignore
        return run_sync(cls.get_user_id(token))

    @classmethod
    async def remove_session(cls, token: str):
        await cls.delete().where(cls.token == token).run() # type: ignore

    @classmethod
    def remove_session_sync(cls, token: str):
        return run_sync(cls.remove_session(token))