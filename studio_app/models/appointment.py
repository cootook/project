import datetime
from flask_security import hash_password
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..config import Config
from .base import data_base


class AppointmentModel(data_base.Model):
    """
    column 'service' value is list of Service.name as JSON str. this field to be moved in dedicated table
    """
    __tablename__ = "appointment"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    service: Mapped[str] # to be moved to dedicated table
    at: Mapped[datetime.datetime]
    price: Mapped[Optional[float]]
    slot_id = mapped_column(ForeignKey("slot.id"))
    amount_time_min: Mapped[int] = mapped_column(default = 90)
    done: Mapped[bool] = mapped_column(default = False)
    done_by_id = mapped_column(ForeignKey("user.id")) 
    done_at: Mapped[Optional[datetime.datetime]]
    approved: Mapped[bool] = mapped_column(default = False)
    approved_by_id = mapped_column(ForeignKey("user.id"))
    approved_at: Mapped[Optional[datetime.datetime]] 
    canceled: Mapped[bool] = mapped_column(default = False)
    canceled_by_id = mapped_column(ForeignKey("user.id"))
    canceled_at: Mapped[Optional[datetime.datetime]]
    last_update_at: Mapped[Optional[datetime.datetime]]
    last_update_by_id = mapped_column(ForeignKey("user.id"))
    description: Mapped[str] = mapped_column(default = "")
    sms_confirmation_code: Mapped[Optional[str]] # to be moved to dedicated table
    phone_confirmed: Mapped[Optional[bool]] = mapped_column(default = False) # to be moved to dedicated table
    confirmed_by_client: Mapped[Optional[bool]] = mapped_column(default = False)
    canceled_by_client: Mapped[Optional[bool]] = mapped_column(default = False)
