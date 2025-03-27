from .roles_seeder import seed_roles
from .admin_user_seeder import seed_admin
from .test_user_seeder import seed_test_user
from flask_sqlalchemy import SQLAlchemy
from ..models.base import data_base


class Seeder:
    def __init__(self, seeders: dict=None, db_session: SQLAlchemy=None):
        self.seeders = seeders or {
            'roles': seed_roles,
            'admin': seed_admin,
            'test_user': seed_test_user
        }
        self.db_session = db_session or data_base
    
    def add_seeder(self, name, seeder_func):
        self.seeders[name] = seeder_func
        
    def seed(self, seeder_name=None):
        if seeder_name:
            if seeder_name not in self.seeders:
                raise ValueError(f"Unknown seeder: {seeder_name}")
            self.seeders[seeder_name](self.db_session)
        else:
            self.seed_all(self.db_session)
            
    def seed_all(self):
        for seeder in self.seeders.values():
            seeder(self.db_session)