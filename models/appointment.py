import datetime
from flask_security import hash_password
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import List, Optional
from ..studio_app.config import Config
from .base import db_base


class AppointmentMode(db_base.Model):
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
    lust_update_at: Mapped[Optional[datetime.datetime]]
    lust_update_by_id = mapped_column(ForeignKey("user.id"))
    description: Mapped[str] = mapped_column(default = "")
    sms_confirmation_code: Mapped[Optional[str]] # to be moved to dedicated table
    phone_confirmed: Mapped[Optional[bool]] = mapped_column(default = False) # to be moved to dedicated table
    confirmed_by_client: Mapped[Optional[bool]] = mapped_column(default = False)
    canceled_by_client: Mapped[Optional[bool]] = mapped_column(default = False)

    @staticmethod
    def create(user_id, service, date_time, slot_id, description):
        """
        this should be called via
        with app.app_context():
        """
        new_appointment = AppointmentMode(user_id=user_id, service = service, at=date_time, slot_id=slot_id, description=description )
        db_base.session.add(new_appointment)
        db_base.session.commit()
        AppointmentMode.set_get_confirmation_code(new_appointment.id)
        return new_appointment
    
    @staticmethod
    def get_by_id(id):
        return db_base.session.scalar(select(AppointmentMode).where(AppointmentMode.id == id))

    @staticmethod
    def set_get_confirmation_code(appointment_id):
        sms_confirmation_code = randrange(1000, 9999, 11)
        db_base.session.execute(update(AppointmentMode).where(AppointmentMode.id == appointment_id).values(sms_confirmation_code = sms_confirmation_code))
        db_base.session.commit()
        return sms_confirmation_code
    
    @staticmethod
    def set_phone_confirmed(appointment_id):
        db_base.session.execute(update(AppointmentMode).where(AppointmentMode.id == appointment_id).values(phone_confirmed = True))
