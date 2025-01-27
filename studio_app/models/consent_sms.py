import datetime
from flask_security import hash_password
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..config import Config
from .base import db_base


class ConsentSmsModel(db_base.Model):
    __tablename__ = "consent_sms"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    user_phone: Mapped[str] = mapped_column(unique = True)
    opted_in: Mapped[bool] = mapped_column(default = False)
    opted_in_at: Mapped[Optional[datetime.datetime]]
    opted_out: Mapped[bool] = mapped_column(default = False)
    opted_out_at: Mapped[Optional[datetime.datetime]]
    terms_version: Mapped[Optional[str]]
    user_agent: Mapped[Optional[str]]
    app_name: Mapped[Optional[str]]
    appVersion: Mapped[Optional[str]]
    platform: Mapped[Optional[str]]
