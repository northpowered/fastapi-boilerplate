"""
Import all of the Tables subclasses in your app here, and register them with
the APP_CONFIG.
"""

import os

from piccolo.conf.apps import AppConfig

from .models import(
    User,
    Role, 
    Group,  
    M2MUserGroup, 
    M2MUserRole, 
    Permission, 
    Policy 
) 
from .authentication.models import Sessions
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="accounting",
    migrations_folder_path=os.path.join(
        CURRENT_DIRECTORY, "piccolo_migrations"
    ),
    table_classes=[
        User,
        Sessions,
        Role,
        Group,
        Permission,
        Policy,
        M2MUserGroup,
        M2MUserRole
    ],
    migration_dependencies=[],
    commands=[],
)
