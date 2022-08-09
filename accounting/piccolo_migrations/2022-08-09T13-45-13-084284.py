from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.query.methods.raw import Raw

ID = "2022-08-09T13:45:13:084284"
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
                year=2022, month=8, day=8, hour=13, second=12, microsecond=948628
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=13, second=24, microsecond=715875
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
                year=2022, month=8, day=8, hour=13, second=12, microsecond=948710
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=13, second=24, microsecond=715952
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
    )
    def run():
        q = "CREATE UNIQUE INDEX unique_column1_column2 ON mytable(column1, column2)"
        Raw()
    manager.add_raw()
    return manager
