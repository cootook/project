from ..models.base import db_base
from ..models.user import UserModel
from ..models.role import RoleModel
from flask_security import hash_password, SQLAlchemyUserDatastore
from ..config import Config
from sqlalchemy import select


def seed_test_user():
    user_datastore = SQLAlchemyUserDatastore(db_base, UserModel, RoleModel)
    if db_base.session.scalar(select(UserModel).where(UserModel.id == 2)) is None:
        test_user = user_datastore.create_user(
            email = Config.TEST_USER_EMAIL, 
            password = hash_password(Config.TEST_USER_PASSWORD), 
            name = Config.TEST_USER_NAME, 
            tel = Config.TEST_USER_US_PHONE, 
            us_phone_number = Config.TEST_USER_US_PHONE
            )
        db_base.session.add(test_user)
        db_base.session.commit()
        user_datastore.add_role_to_user(test_user, "tester")
        db_base.session.commit()
        print("created: ", db_base.session.scalar(select(UserModel).where(UserModel.id == 2)))
    else:
        print("already exist: ", db_base.session.scalar(select(UserModel).where(UserModel.id == 2)))