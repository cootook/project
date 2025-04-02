from ..models.base import data_base
from ..models.user import UserModel
from ..models.role import RoleModel
from ..repositories.user_repository import UserRepository
from flask_security import hash_password, SQLAlchemyUserDatastore
from ..config import Config
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy


def seed_admin(db_session: SQLAlchemy=data_base, config=Config):
    user_datastore = SQLAlchemyUserDatastore(db_session, UserModel, RoleModel)
    if db_session.session.scalar(select(UserModel).where(UserModel.id == 1)) is None:
        repo = UserRepository()
        admin = repo.create_user(
            email = config.ADMINISTRATOR_EMAIL, 
            password = hash_password(config.ADMINISTRATOR_PASSWORD), 
            name = config.ADMINISTRATOR_NAME, 
            tel = config.ADMINISTRATOR_US_PHONE, 
            us_phone_number = config.ADMINISTRATOR_US_PHONE
            )
        user_datastore.add_role_to_user(admin, "admin")
        db_session.session.commit()
        print("created: ", db_session.session.scalar(select(UserModel).where(UserModel.id == 1)))
    else:
        print("already exist: ", db_session.session.scalar(select(UserModel).where(UserModel.id == 1)))

def restore_first_admin(db_session=data_base, config=Config):
    repo = UserRepository(db_session)
    admin = repo.get_user_by_id(1)
    if admin:        
        repo.update_user_data(
            admin,
            email = config.ADMINISTRATOR_EMAIL, 
            password = hash_password(config.ADMINISTRATOR_PASSWORD), 
            name = config.ADMINISTRATOR_NAME, 
            tel = config.ADMINISTRATOR_US_PHONE, 
            us_phone_number = config.ADMINISTRATOR_US_PHONE
        )
        print("admin_user_seeder SUCCESS: values restored from config")
    else:
        print("admin_user_seeder ERROR: the first admin does not exist")