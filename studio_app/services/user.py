from ..db_classes import User
from flask_security import current_user, hash_password, login_user, logout_user
from ..config import Config

class User_service:
    def __init__(self):
        pass

    @classmethod
    def login_by_id(cls, id):
        user = User.get_user_by_id(id)
        logout_user()
        return login_user(user)