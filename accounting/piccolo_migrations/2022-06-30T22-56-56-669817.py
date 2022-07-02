from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2022-06-30T22:56:56:669817"
VERSION = "0.80.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="", description=DESCRIPTION
    )

    def run():
        print(f"running {ID}")

    manager.add_raw(run)

    return manager
