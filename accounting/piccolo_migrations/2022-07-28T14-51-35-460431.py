from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import UUID
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.columns.defaults.uuid import UUID4


ID = "2022-07-28T14:51:35:460431"
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
                year=2022, month=7, day=7, hour=14, second=35, microsecond=329481
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=7, day=7, hour=14, second=14, microsecond=691068
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
                year=2022, month=7, day=7, hour=14, second=35, microsecond=329559
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2022, month=7, day=7, hour=14, second=14, microsecond=691144
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    manager.alter_column(
        table_class_name="Role",
        tablename="roles",
        column_name="id",
        params={"default": "75897aa6-01a8-4cfc-877a-ea1137f86d4e"},
        old_params={"default": "c7345154-d99f-4cf3-89f9-cd05384dae77"},
        column_class=Text,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="Group",
        tablename="groups",
        column_name="id",
        params={"default": UUID4()},
        old_params={"default": ""},
        column_class=UUID,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="Permission",
        tablename="permissions",
        column_name="id",
        params={"default": "5830793f-b63f-48da-8268-797058b5c6d6"},
        old_params={"default": "50e40c6b-76c9-446d-85d3-f17956353980"},
        column_class=Text,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="Policy",
        tablename="policies",
        column_name="id",
        params={"default": "2bc279b2-7ce6-45f0-b01b-0dd6982012c8"},
        old_params={"default": "5c02d8fb-d59d-499a-897e-df469afdef88"},
        column_class=Text,
        old_column_class=Text,
    )

    return manager
