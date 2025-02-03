from ..models.base import db_base
from ..models.user import UserModel
from ..models.role import RoleModel
from ..repositories.user_repository import UserRepository
from flask_security import hash_password, SQLAlchemyUserDatastore
from ..config import Config
from sqlalchemy import select


def seed_admin():
    user_datastore = SQLAlchemyUserDatastore(db_base, UserModel, RoleModel)
    if db_base.session.scalar(select(UserModel).where(UserModel.id == 1)) is None:
        repo = UserRepository()
        admin = repo.create_user(
            email = Config.ADMINISTRATOR_EMAIL, 
            password = hash_password(Config.ADMINISTRATOR_PASSWORD), 
            name = Config.ADMINISTRATOR_NAME, 
            tel = Config.ADMINISTRATOR_US_PHONE, 
            us_phone_number = Config.ADMINISTRATOR_US_PHONE
            )
        user_datastore.add_role_to_user(admin, "admin")
        db_base.session.commit()
        print("created: ", db_base.session.scalar(select(UserModel).where(UserModel.id == 1)))
    else:
        print("already exist: ", db_base.session.scalar(select(UserModel).where(UserModel.id == 1)))