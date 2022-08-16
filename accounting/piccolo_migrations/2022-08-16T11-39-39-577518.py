from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from accounting.users.models import foo
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.columns.defaults.timestamp import TimestampNow


ID = "2022-08-16T11:39:39:577518"
VERSION = "0.82.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accounting", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="created_at",
        params={"default": TimestampNow()},
        old_params={"default": foo},
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="updated_at",
        params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=11, second=39, microsecond=442940
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=11, second=32, microsecond=809724
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    return manager
