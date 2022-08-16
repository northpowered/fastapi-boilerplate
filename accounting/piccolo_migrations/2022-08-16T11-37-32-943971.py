from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom


ID = "2022-08-16T11:37:32:943971"
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
        params={"nullable": True},
        old_params={"nullable": False},
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="updated_at",
        params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=11, second=32, microsecond=809724
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=11, second=3, microsecond=935351
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    return manager
