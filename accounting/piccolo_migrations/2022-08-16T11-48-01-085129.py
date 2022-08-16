from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2022-08-16T11:48:01:085129"
VERSION = "0.82.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accounting", description=DESCRIPTION
    )

    manager.drop_column(
        table_class_name="User",
        tablename="users",
        column_name="updated_at",
        db_column_name="updated_at",
    )

    return manager
