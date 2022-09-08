from email.mime import base
from fastapi import HTTPException
from asyncpg.exceptions import IntegrityConstraintViolationError
from pprint import pprint


class IntegrityException(HTTPException):
    def __init__(self, base_exception: IntegrityConstraintViolationError):
        try:
            detail = base_exception.args[0]
        except (KeyError, TypeError, ValueError):
            detail = base_exception.message
        finally:
            raise HTTPException(
                status_code=400,
                detail=detail
            )


class ObjectNotFoundException(HTTPException):
    def __init__(self, object_name: str, object_id: str):
        raise HTTPException(
            status_code=404,
            detail=f'Object {object_name} with id {object_id} not found'
        )


class BaseBadRequestException(HTTPException):
    def __init__(self, message: str):
        raise HTTPException(
            status_code=400,
            detail=str(message)
        )


class UnauthorizedException(HTTPException):
    def __init__(self, details: str):
        raise HTTPException(
            status_code=401,
            detail=str(details)
        )


class PermissionDeniedException(HTTPException):
    def __init__(self, details: str):
        raise HTTPException(
            status_code=403,
            detail=str(details)
        )
