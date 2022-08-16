from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom


ID = "2022-08-16T11:14:41:221323"
VERSION = "0.82.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accounting", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="email",
        params={"unique": True},
        old_params={"unique": False},
        column_class=Text,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="created_at",
        params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=11, second=41, microsecond=83965
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=10, second=53, microsecond=315760
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
                year=2022, month=8, day=8, hour=11, second=41, microsecond=84042
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=10, second=53, microsecond=315964
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    return manager
