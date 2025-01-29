from ..models.base import db_base
from ..models.user import UserModel
from ..models.role import RoleModel
from flask_security import hash_password, verify_and_update_password
from ..config import Config
from ..webapp import user_datastore
from sqlalchemy import select



def seed_admin():
    from ..webapp import user_datastore
    if db_base.session.scalar(select(UserModel).where(UserModel.id == 1)) is None:
        admin_email = Config.ADMINISTRATOR_EMAIL
        admin_password = Config.ADMINISTRATOR_PASSWORD
        admin_name = Config.ADMINISTRATOR_NAME
        admin_phone = Config.ADMINISTRATOR_US_PHONE
        admin = user_datastore.create_user(
            email = admin_email, 
            password = hash_password(admin_password), 
            name = admin_name, 
            tel = admin_phone, 
            us_phone_number = admin_phone
            )
        db_base.session.add(admin)
        db_base.session.commit()

        user_datastore.add_role_to_user(admin, "admin")
        db_base.session.commit()
        print("created: ", db_base.session.scalar(select(UserModel).where(UserModel.id == 1)))
    else:
        print("already exist: ", db_base.session.scalar(select(UserModel).where(UserModel.id == 1)))