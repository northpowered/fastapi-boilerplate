from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom


ID = "2022-08-02T15:46:54:565956"
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
        params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=15, second=54, microsecond=413948
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=15, second=23, microsecond=389137
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="updated_at",
        params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=15, second=54, microsecond=414023
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=15, second=23, microsecond=389229
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    return manager
