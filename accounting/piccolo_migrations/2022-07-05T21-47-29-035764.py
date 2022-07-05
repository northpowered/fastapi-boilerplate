from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Secret
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamptz
from piccolo.columns.defaults.timestamptz import TimestamptzCustom


ID = "2022-07-05T21:47:29:035764"
VERSION = "0.80.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="user", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="password",
        params={"length": 255, "secret": True},
        old_params={"length": None, "secret": False},
        column_class=Secret,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="created_at",
        params={
            "default": TimestamptzCustom(
                year=2022, month=7, day=7, hour=21, second=29, microsecond=20680
            )
        },
        old_params={
            "default": TimestamptzCustom(
                year=2022, month=7, day=7, hour=16, second=35, microsecond=588373
            )
        },
        column_class=Timestamptz,
        old_column_class=Timestamptz,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="updated_at",
        params={
            "default": TimestamptzCustom(
                year=2022, month=7, day=7, hour=21, second=29, microsecond=20757
            )
        },
        old_params={
            "default": TimestamptzCustom(
                year=2022, month=7, day=7, hour=16, second=35, microsecond=588544
            )
        },
        column_class=Timestamptz,
        old_column_class=Timestamptz,
    )

    return manager
