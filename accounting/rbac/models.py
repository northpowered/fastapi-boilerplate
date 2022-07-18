from uuid import uuid4
import datetime
from loguru import logger
from typing import TypeVar, Type, Optional
from piccolo.table import Table
from piccolo.columns import Timestamp, m2m
from piccolo.columns.column_types import (
    Text, Boolean, Timestamp, ForeignKey,
    LazyTableReference
)
from asyncpg.exceptions import UniqueViolationError
from utils.exceptions import IntegrityException, ObjectNotFoundException, BaseBadRequestException
from configuration import config
from piccolo.columns.readable import Readable
from accounting import User, Role, Group

T_P = TypeVar('T_P', bound='Policy')
T_Pm = TypeVar('T_Pm', bound='Permission')

tz: datetime.timezone = config.main.tz

class Permission(Table, tablename="permissions"):

    id = Text(primary_key=True, index=True)
    name = Text(unique=True, index=False, null=False)
    object = Text(unique=True, index=True, null=False)
    description = Text(unique=False, index=False, null=True)
    policies = m2m.M2M(LazyTableReference("Policy", module_path=__name__))


class M2MUserRole(Table):
    user = ForeignKey(User)
    role = ForeignKey(Role)

class M2MUserGroup(Table):
    user = ForeignKey(User)
    group = ForeignKey(Group)

class Policy(Table, tablename="policies"):
    id = Text(primary_key=True, index=True)
    permission = ForeignKey(Permission)
    role = ForeignKey(Role)