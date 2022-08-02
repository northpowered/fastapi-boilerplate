from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom
from utils.piccolo import uuid4_for_PK


ID = "2022-08-02T15:36:00:644882"
VERSION = "0.82.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accounting", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="id",
        params={"default": uuid4_for_PK},
        old_params={"default": ""},
        column_class=Text,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="created_at",
        params={
            "default": TimestampCustom(
                year=2022, month=8, day=8, hour=15, second=0, microsecond=493642
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
                year=2022, month=8, day=8, hour=15, second=0, microsecond=493715
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
        params={"default": uuid4_for_PK},
        old_params={"default": ""},
        column_class=Text,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="Group",
        tablename="groups",
        column_name="id",
        params={"default": uuid4_for_PK},
        old_params={"default": ""},
        column_class=Text,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="Permission",
        tablename="permissions",
        column_name="id",
        params={"default": uuid4_for_PK},
        old_params={"default": "f8d30782-2ec5-4db7-a751-838afe607743"},
        column_class=Text,
        old_column_class=Text,
    )

    manager.alter_column(
        table_class_name="Policy",
        tablename="policies",
        column_name="id",
        params={"default": uuid4_for_PK},
        old_params={"default": ""},
        column_class=Text,
        old_column_class=Text,
    )

    return manager
