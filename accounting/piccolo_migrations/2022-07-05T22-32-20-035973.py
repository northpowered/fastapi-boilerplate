from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import Timestamptz
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.columns.defaults.timestamptz import TimestamptzCustom
from piccolo.columns.defaults.timestamptz import TimestamptzNow


ID = "2022-07-05T22:32:20:035973"
VERSION = "0.80.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="user", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="created_at",
        params={
            "default": TimestampCustom(
                year=2022, month=7, day=7, hour=22, second=20, microsecond=23583
            )
        },
        old_params={
            "default": TimestamptzCustom(
                year=2022, month=7, day=7, hour=22, second=46, microsecond=486563
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamptz,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="updated_at",
        params={
            "default": TimestampCustom(
                year=2022, month=7, day=7, hour=22, second=20, microsecond=23670
            )
        },
        old_params={
            "default": TimestamptzCustom(
                year=2022, month=7, day=7, hour=22, second=46, microsecond=486687
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamptz,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="last_login",
        params={"default": TimestampNow()},
        old_params={"default": TimestamptzNow()},
        column_class=Timestamp,
        old_column_class=Timestamptz,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="birthdate",
        params={"default": TimestampNow()},
        old_params={"default": TimestamptzNow()},
        column_class=Timestamp,
        old_column_class=Timestamptz,
    )

    return manager
