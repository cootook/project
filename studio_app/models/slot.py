import datetime
import os
from flask_security import hash_password
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..config import Config
from .base import db_base


class SlotModel(db_base.Model):
    __tablename__ = "slot"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date]
    time: Mapped[datetime.time]
    opened: Mapped[bool] = mapped_column(default = False)
    opened_by_id = mapped_column(ForeignKey("user.id", use_alter=True), nullable=True)
    opened_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    occupied: Mapped[bool] = mapped_column(nullable=True)
    occupied_by_appoint_id = mapped_column(ForeignKey("appointment.id", use_alter=True), nullable=True)
