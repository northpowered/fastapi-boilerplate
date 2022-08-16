from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2022-08-16T11:56:14:163143"
VERSION = "0.82.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accounting", description=DESCRIPTION
    )

    manager.drop_column(
        table_class_name="User",
        tablename="users",
        column_name="birthdate",
        db_column_name="birthdate",
    )

    return manager
