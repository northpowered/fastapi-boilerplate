"""
Import all of the Tables subclasses in your app here, and register them with
the APP_CONFIG.
"""

import os

from piccolo.conf.apps import AppConfig

from .rbac import (
    M2MUserGroup,
    M2MUserRole,
    Permission,
    Policy
)
from .users import User
from .groups import Group
from .roles import Role
from .authentication import Sessions
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
