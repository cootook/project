from .roles_seeder import seed_roles
from .users_seeder import seed_users

def run_all_seeds():
    seed_roles()
    seed_users()

if __name__ == "__main__":
    run_all_seeds()