from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


data_base = SQLAlchemy(model_class=Base)

fsqla.FsModels.set_db_info(data_base)