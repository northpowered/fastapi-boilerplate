from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2022-08-09T13:54:26:519696"
VERSION = "0.82.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="", description=DESCRIPTION
    )

    def run():
        print(f"running {ID}")

    manager.add_raw(run)

    return manager
