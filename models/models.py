import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_security import hash_password
from flask_security.models import fsqla_v3 as fsqla
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..config import Config

class Base(DeclarativeBase):
    pass

db_base = SQLAlchemy(model_class=Base)

fsqla.FsModels.set_db_info(db_base)