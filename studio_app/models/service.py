import datetime
from flask_security import hash_password
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..config import Config
from .base import db_base


class ServiceModel(db_base.Model):
    __tablename__ = "service"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")
    deleted: Mapped[bool] = mapped_column(default = False)

