from .payload_models import UserModel, RoleModel, GroupModel

test_superuser_1: UserModel = UserModel.create()
test_superuser_2: UserModel = UserModel.create()
test_user_1: UserModel = UserModel.create()
test_user_2: UserModel = UserModel.create()
test_role_1: RoleModel = RoleModel(name='test_role_1')
test_role_2: RoleModel = RoleModel(name='test_role_2')
test_group_1: GroupModel = GroupModel(name='test_group_1')
test_group_2: GroupModel = GroupModel(name='test_group_2')
