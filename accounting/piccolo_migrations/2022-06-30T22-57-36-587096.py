from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Boolean
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.columns.indexes import IndexMethod


ID = "2022-06-30T22:57:36:587096"
VERSION = "0.80.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accounting", description=DESCRIPTION
    )

    manager.add_table("User", tablename="users")

    manager.add_column(
        table_class_name="User",
        tablename="users",
        column_name="id",
        db_column_name="id",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": True,
            "unique": False,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="users",
        column_name="username",
        db_column_name="username",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": True,
            "index": True,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="users",
        column_name="email",
        db_column_name="email",
        column_class_name="Text",
        column_class=Text,
        params={
            "nullable": True,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="users",
        column_name="password",
        db_column_name="password",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="users",
        column_name="active",
        db_column_name="active",
        column_class_name="Boolean",
        column_class=Boolean,
        params={
            "nullable": False,
            "default": True,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="users",
        column_name="created_at",
        db_column_name="created_at",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "nullable": False,
            "default": TimestampCustom(
                year=2022, month=6, day=6, hour=22, second=36, microsecond=585778
            ),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="users",
        column_name="updated_at",
        db_column_name="updated_at",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "nullable": False,
            "default": TimestampCustom(
                year=2022, month=6, day=6, hour=22, second=36, microsecond=585843
            ),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="users",
        column_name="last_login",
        db_column_name="last_login",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "nullable": True,
            "default": TimestampNow(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="User",
        tablename="users",
        column_name="birthdate",
        db_column_name="birthdate",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "nullable": True,
            "default": TimestampNow(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    return manager
