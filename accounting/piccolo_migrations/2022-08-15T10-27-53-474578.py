from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom


ID = "2022-08-15T10:27:53:474578"
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
                year=2022, month=8, day=8, hour=10, second=53, microsecond=315760
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=10, second=17, microsecond=194707
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
                year=2022, month=8, day=8, hour=10, second=53, microsecond=315964
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=10, second=17, microsecond=194782
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    return manager
