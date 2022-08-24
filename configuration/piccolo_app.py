"""
Import all of the Tables subclasses in your app here, and register them with
the APP_CONFIG.

IMPORTANT!
Do NOT change this file
This piccolo_app is only for a right drop/init management of CLI app
"""

import os

from piccolo.conf.apps import AppConfig

from piccolo.apps.migrations.tables import Migration

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="configuration",
    migrations_folder_path=os.path.join(
        CURRENT_DIRECTORY, "piccolo_migrations"
    ),
    table_classes=[
        Migration
    ],
    migration_dependencies=[],
    commands=[],
)
