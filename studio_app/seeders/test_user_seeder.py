from ..models.base import db_base
from ..models.user import UserModel
from ..models.role import RoleModel
from flask_security import hash_password, SQLAlchemyUserDatastore
from ..config import Config
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy


def seed_test_user(db_session: SQLAlchemy=db_base, config=Config):
    user_datastore = SQLAlchemyUserDatastore(db_session, UserModel, RoleModel)
    if db_session.session.scalar(select(UserModel).where(UserModel.id == 2)) is None:
        test_user = user_datastore.create_user(
            email = config.TEST_USER_EMAIL, 
            password = hash_password(config.TEST_USER_PASSWORD), 
            name = config.TEST_USER_NAME, 
            tel = config.TEST_USER_US_PHONE, 
            us_phone_number = config.TEST_USER_US_PHONE
            )
        db_session.session.add(test_user)
        db_session.session.commit()
        user_datastore.add_role_to_user(test_user, "tester")
        db_session.session.commit()
        print("created: ", db_session.session.scalar(select(UserModel).where(UserModel.id == 2)))
    else:
        print("already exist: ", db_session.session.scalar(select(UserModel).where(UserModel.id == 2)))