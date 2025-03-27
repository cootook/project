from flask_security.models import fsqla_v3 as fsqla
from random import randrange
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from .base import data_base


class RoleModel(data_base.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")
