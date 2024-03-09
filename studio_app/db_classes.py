import datetime

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class Appointment(Base):
    __tablename__ = "appointment"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="appointment")
    service_id = mapped_column(ForeignKey("service.id"))
    at: Mapped[datetime.datetime]
    price: Mapped[Optional[float]]
    deposit_needed: Mapped[bool] = mapped_column(default=False)
    deposit: Mapped[Optional[float]]
    slot_id = mapped_column(ForeignKey("slot.id"))
    amount_time_min: Mapped[int] = mapped_column(default = 90)
    done: Mapped[bool] = mapped_column(default = False)
    done_by = mapped_column(ForeignKey("user.id")) 
    done_at: Mapped[Optional[datetime.datetime]]
    approved: Mapped[bool] = mapped_column(default = False)
    approved_by = mapped_column(ForeignKey("user.id"))
    approved_at: Mapped[Optional[datetime.datetime]] 
    canceled: Mapped[bool] = mapped_column(default = False)
    canceled_by = mapped_column(ForeignKey("user.id"))
    canceled_at: Mapped[Optional[datetime.datetime]]
    lust_update_at: Mapped[Optional[datetime.datetime]]
    lust_update_by = mapped_column(ForeignKey("user.id"))
    description: Mapped[str] = mapped_column(default = "")

class Booking_message:
    __tablename__ = "booking_message"
    id: Mapped[int] = mapped_column(primary_key=True)
    appoint_id = mapped_column(ForeignKey("appointment.id"))
    author_id = mapped_column(ForeignKey("user.id"))
    at: Mapped[datetime.datetime]
    edited_at: Mapped[Optional[datetime.datetime]]
    deleted: Mapped[bool] = mapped_column(default = False)

class Language:
    __tablename__ = "language"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Mf_recovery_code:
    __tablename__ = "mf_recovery_code"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates = "mf_recovery_codes")

class Notification_type:
    __tablename__ = "notification_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Payment:
    __tablename__ = "payment"
    id: Mapped[int] = mapped_column(primary_key=True)
    method_id = mapped_column(ForeignKey("payment_method.id"))
    type_id = mapped_column(ForeignKey("payment_type.id"))
    amount: Mapped[float]
    payed: Mapped[bool] = mapped_column(default = False)
    status_id: Mapped[int]
    accepted_by: Mapped[int]
    payed_by: Mapped[int]
    at: Mapped[datetime.datetime]
    lust_update_at: Mapped[Optional[datetime.datetime]]
    lust_update_by: Mapped[Optional[int]]
    description: Mapped[str] = mapped_column(default = "")

class Payment_method:
    __tablename__ = "payment_method"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Payment_status:
    __tablename__ = "payment_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Payment_type:
    __tablename__ = "payment_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Role:
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Service:
    __tablename__ = "service"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Service_role:
    __tablename__ = "service_role"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int]
    role_id: Mapped[int]

class Slot:
    __tablename__ = "slot"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime.datetime]
    opened: Mapped[bool]
    opened_by = mapped_column(ForeignKey("user.id"))
    opened_at: Mapped[datetime.datetime]
    occupied: Mapped[bool]
    occupied_by_appoint = mapped_column(ForeignKey("appointment.id"))

class User:
    _tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique = True)
    password: Mapped[Optional[str]]
    active: Mapped[str] = mapped_column(default = True)
    fs_uniquifier: Mapped[str] = mapped_column(unique = True) 
    confirmed_at: Mapped[Optional[datetime.datetime]]
    last_login_at: Mapped[Optional[datetime.datetime]]
    current_login_at: Mapped[Optional[datetime.datetime]]
    last_login_ip: Mapped[str] 
    current_login_ip: Mapped[str] 
    login_count: Mapped[int] 
    mf_recovery_codes: Mapped[List["Mf_recovery_code"]] = relationship(back_populates = "user")
    name: Mapped[str]   
    instagram: Mapped[str] 
    tel: Mapped[Optional[str]]
    language_id = mapped_column(ForeignKey("language.id")) 
    internal_description: Mapped[str] = mapped_column(unique = True) 
    picture_path: Mapped[str] = mapped_column(unique = True) 
    appointment: Mapped[List["Appointment"]] = relationship(back_populates = "user")
    role: Mapped[List["User_role"]] = relationship(back_populates = "user")
    lust_update_at: Mapped[datetime.datetime] 
    lust_update_by = mapped_column(ForeignKey("user.id"))
    deleted: Mapped[bool] = mapped_column(default = False)
    deleted_at: Mapped[Optional[datetime.datetime]]
    deleted_by = mapped_column(ForeignKey("user.id"))

class User_notification:
    __tablename__ = "user_notification"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    type_id = mapped_column(ForeignKey("notification_type"))

class User_role:
    __tablename__ = "user_role"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates = "role")
    role_id = mapped_column(ForeignKey("role.id"))
    set_by = mapped_column(ForeignKey("user.id"))
    set_at: Mapped[datetime.datetime]