from ..models.base import db_base
from ..models.user import UserModel
from ..repositories.user_repository import UserRepository
from flask_security import hash_password, verify_and_update_password
from ..config import Config
from ..webapp import user_datastore
from sqlalchemy import select


def seed_admin():
    from ..webapp import user_datastore
    if db_base.session.scalar(select(UserModel).where(UserModel.id == 1)) is None:
        admin = UserRepository.create_user(
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