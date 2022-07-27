import loguru
from .authentication.jwt import get_user_by_token
from fastapi import Depends, Request
from functools import wraps

from accounting.rbac.checks import check_user_endpoint_policy
from utils.exceptions import PermissionDeniedException
from loguru import logger



def AAA_endpoint_oauth2():
    from . import User
    def outer_wrapper(func):
        @wraps(func)
        async def wrapper(request: Request,current_user: User, *args, **kwargs):
            try:
                assert await check_user_endpoint_policy(current_user,func.__name__),"Permission denied"
            except AssertionError as ex:
                raise PermissionDeniedException(str(ex))
            else:
                logger.debug(f'Permission denied | User: {current_user.username} | Object: {func.__name__}')
            return await func(request,current_user, *args, **kwargs)

        return wrapper
    return outer_wrapper