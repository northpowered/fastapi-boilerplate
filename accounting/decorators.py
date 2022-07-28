from fastapi import Request
from functools import wraps
from utils.exceptions import PermissionDeniedException
from loguru import logger

def AAA_endpoint_oauth2():
    from .users import User
    def outer_wrapper(func):
        func.__setattr__('rbac_enable',True) #Need for openapi schema, to show, that endpoint needs a permission
        @wraps(func)
        async def wrapper(request: Request,current_user: User, *args, **kwargs):
            from accounting.rbac.checks import check_user_endpoint_policy
            try:
                assert await check_user_endpoint_policy(current_user,func.__name__),"Permission denied"
            except AssertionError as ex:
                raise PermissionDeniedException(str(ex))
            else:
                logger.debug(f'Permission denied | User: {current_user.username} | Object: {func.__name__}')
            return await func(request,current_user, *args, **kwargs)
        return wrapper
    return outer_wrapper