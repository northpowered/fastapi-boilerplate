from .payload_models import UserModel

test_superuser_1: UserModel = UserModel.create()
test_superuser_2: UserModel = UserModel.create()
test_user_1: UserModel = UserModel.create()
test_user_2: UserModel = UserModel.create()