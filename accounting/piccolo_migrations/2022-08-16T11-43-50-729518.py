from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp


ID = "2022-08-16T11:43:50:729518"
VERSION = "0.82.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accounting", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="users",
        column_name="updated_at",
        params={"nullable": True},
        old_params={"nullable": False},
        column_class=Timestamp,
        old_column_class=Timestamp,
    )

    return manager
