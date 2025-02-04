from flask_security import SQLAlchemyUserDatastore
from ..models.base import db_base
from ..models.user import UserModel
from ..models.role import RoleModel
from ..config import Config
from flask_sqlalchemy import SQLAlchemy


class BaseRepository():
    """
    injects dependencies into child classes:
        db: SQLAlchemy=from ..models.base import db_base, 
        user_store: SQLAlchemyUserDatastore=None, 
        config=from ..config import Config)
    """
    def __init__(
            self, 
            db: SQLAlchemy=db_base, 
            user_store: SQLAlchemyUserDatastore=None, 
            config=None):
        self.db = db.session
        self.user_store = user_store or SQLAlchemyUserDatastore(db_base, UserModel, RoleModel)
        self.config = config or Config
