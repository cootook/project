import datetime
from flask_security import hash_password
from flask_security.models import fsqla_v3 as fsqla
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..studio_app.config import Config
from .base import db_base


class RoleModel(db_base.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")
