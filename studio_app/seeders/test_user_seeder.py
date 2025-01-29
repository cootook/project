from ..models.base import db_base
from ..models.user import UserModel
from flask_security import hash_password, verify_and_update_password
from ..config import Config
from ..webapp import user_datastore
from sqlalchemy import select



def seed_test_user():
    if db_base.session.scalar(select(UserModel).where(UserModel.id == 2)) is None:
        test_user_email = Config.TEST_USER_EMAIL
        test_user_password = Config.TEST_USER_PASSWORD
        test_user_name = Config.TEST_USER_NAME
        test_user_phone = Config.TEST_USER_US_PHONE
        test_user = user_datastore.create_user(
            email = test_user_email, 
            password = hash_password(test_user_password), 
            name = test_user_name, 
            tel = test_user_phone, 
            us_phone_number = test_user_phone
            )
        db_base.session.add(test_user)
        db_base.session.commit()

        user_datastore.add_role_to_user(test_user, "tester")
        db_base.session.commit()
        print("created: ", db_base.session.scalar(select(UserModel).where(UserModel.id == 2)))
    else:
        print("already exist: ", db_base.session.scalar(select(UserModel).where(UserModel.id == 2)))