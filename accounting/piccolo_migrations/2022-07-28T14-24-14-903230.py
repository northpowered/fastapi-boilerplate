from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom


ID = "2022-07-28T14:24:14:903230"
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
                year=2022, month=7, day=7, hour=14, second=14, microsecond=691068
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=7, day=7, hour=22, second=43, microsecond=526300
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
                year=2022, month=7, day=7, hour=14, second=14, microsecond=691144
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=7, day=7, hour=22, second=43, microsecond=526381
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    manager.alter_column(
        table_class_name="Role",
        tablename="roles",
        column_name="id",
        params={"default": "c7345154-d99f-4cf3-89f9-cd05384dae77"},
        old_params={"default": ""},
        column_class=Text,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="Permission",
        tablename="permissions",
        column_name="id",
        params={"default": "50e40c6b-76c9-446d-85d3-f17956353980"},
        old_params={"default": "f8d30782-2ec5-4db7-a751-838afe607743"},
        column_class=Text,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="Policy",
        tablename="policies",
        column_name="id",
        params={"default": "5c02d8fb-d59d-499a-897e-df469afdef88"},
        old_params={"default": ""},
        column_class=Text,
        old_column_class=Text,
    )

    return manager
