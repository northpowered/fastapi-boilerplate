from fastapi import Request
from functools import wraps
from utils.exceptions import PermissionDeniedException, UnauthorizedException
from loguru import logger
from .authentication.jwt import get_user_by_token, decode_auth_header
def AAA_endpoint_oauth2():
    from .users import User
    def outer_wrapper(func):
        func.__setattr__('rbac_enable',True) #Need for openapi schema, to show, that endpoint needs a permission
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            from accounting.rbac.checks import check_user_endpoint_policy
            try:
                validator,token = decode_auth_header(request.headers.get('authorization', str()))
                current_user: User = await get_user_by_token(token)
                assert await check_user_endpoint_policy(current_user,func.__name__),"Permission denied"
            except AssertionError as ex:
                logger.debug(f'Access denied | User: {current_user.username} | Object: {func.__name__}')
                raise PermissionDeniedException(str(ex))
            except IndexError as ex:
                raise UnauthorizedException('Cannot decode token')
            else:
                logger.debug(f'Access permitted | User: {current_user.username} | Object: {func.__name__}')
            return await func(request, *args, **kwargs)
        return wrapper
    return outer_wrapper