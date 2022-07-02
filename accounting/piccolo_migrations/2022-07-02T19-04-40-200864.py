from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import Timestamptz
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.columns.defaults.timestamptz import TimestamptzCustom
from piccolo.columns.defaults.timestamptz import TimestamptzNow


ID = "2022-07-02T19:04:40:200864"
VERSION = "0.80.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accounting", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="created_at",
        params={
            "default": TimestamptzCustom(
                year=2022, month=7, day=7, hour=19, second=40, microsecond=199414
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=6, day=6, hour=22, second=36, microsecond=585778
            )
        },
        column_class=Timestamptz,
        old_column_class=Timestamp,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="updated_at",
        params={
            "default": TimestamptzCustom(
                year=2022, month=7, day=7, hour=19, second=40, microsecond=199502
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=6, day=6, hour=22, second=36, microsecond=585843
            )
        },
        column_class=Timestamptz,
        old_column_class=Timestamp,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="last_login",
        params={"default": TimestamptzNow()},
        old_params={"default": TimestampNow()},
        column_class=Timestamptz,
        old_column_class=Timestamp,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="birthdate",
        params={"default": TimestamptzNow()},
        old_params={"default": TimestampNow()},
        column_class=Timestamptz,
        old_column_class=Timestamp,
    )

    return manager
