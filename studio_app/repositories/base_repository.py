from flask_security import SQLAlchemyUserDatastore
from ..models.base import data_base
from ..models.user import UserModel
from ..models.role import RoleModel
from ..config import Config
from flask_sqlalchemy import SQLAlchemy


class BaseRepository():
    """
    injects dependencies into child classes:
        db: SQLAlchemy=from ..models.base import data_base, 
        user_store: SQLAlchemyUserDatastore=None, 
        config=from ..config import Config)
    """
    def __init__(
            self, 
            db: SQLAlchemy=data_base, 
            user_store: SQLAlchemyUserDatastore=None, 
            config=None):
        self.db = db.session
        self.user_store = user_store or SQLAlchemyUserDatastore(data_base, UserModel, RoleModel)
        self.config = config or Config

    def _log_error(self, message: str, exception: Exception = None) -> None:
        error_msg = f"Error: {message}"
        if exception:
            error_msg += f" - {str(exception)}"
        print(error_msg)
