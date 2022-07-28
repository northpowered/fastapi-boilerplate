from .models import Permission, Policy
from accounting.users.models import User
from accounting.roles.models import Role
from configuration import config

async def check_user_endpoint_policy(user: User, endpoint_name: str)->bool:
    if not config.main.is_prod_mode and not config.security.is_rbac_enabled:
        return True
    if user.superuser:
        return True
    for role in user.roles: # type: ignore
        await role.join_m2m()
        for policy in role.policies:
            if endpoint_name == policy.object:
                return True
            else:
                continue
    return False