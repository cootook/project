from .roles_seeder import seed_roles
from .admin_user_seeder import seed_admin
from .test_user_seeder import seed_test_user


class Seeder:
    @staticmethod
    def seed_all():
        seed_roles()
        seed_admin()
        seed_test_user()

    @staticmethod
    def seed_admin():
        seed_admin()

    @staticmethod
    def seed_test_user():
        seed_test_user()

    @staticmethod
    def seed_roles():
        seed_roles()