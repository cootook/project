import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

class Base(DeclarativeBase):
    pass

db_base = SQLAlchemy(model_class=Base)

fsqla.FsModels.set_db_info(db_base)

class Appointment(db_base.Model):
    __tablename__ = "appointment"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(foreign_keys=user_id)
    service_id = mapped_column(ForeignKey("service.id"))
    service = relationship("Service", foreign_keys=[service_id])
    at: Mapped[datetime.datetime]
    price: Mapped[Optional[float]]
    deposit_needed: Mapped[bool] = mapped_column(default=False)
    deposit: Mapped[Optional[float]]
    slot_id = mapped_column(ForeignKey("slot.id"))
    slot = relationship("Slot", foreign_keys=[slot_id])
    amount_time_min: Mapped[int] = mapped_column(default = 90)
    done: Mapped[bool] = mapped_column(default = False)
    done_by_id = mapped_column(ForeignKey("user.id")) 
    done_by = relationship("User", foreign_keys=[done_by_id])
    done_at: Mapped[Optional[datetime.datetime]]
    approved: Mapped[bool] = mapped_column(default = False)
    approved_by_id = mapped_column(ForeignKey("user.id"))
    approved_by = relationship("User", foreign_keys=[approved_by_id])
    approved_at: Mapped[Optional[datetime.datetime]] 
    canceled: Mapped[bool] = mapped_column(default = False)
    canceled_by_id = mapped_column(ForeignKey("user.id"))
    canceled_by = relationship("User", foreign_keys=[canceled_by_id])
    canceled_at: Mapped[Optional[datetime.datetime]]
    lust_update_at: Mapped[Optional[datetime.datetime]]
    lust_update_by_id = mapped_column(ForeignKey("user.id"))
    lust_update_by = relationship("User", foreign_keys=[lust_update_by_id])
    description: Mapped[str] = mapped_column(default = "")

class Booking_message(db_base.Model):
    __tablename__ = "booking_message"
    id: Mapped[int] = mapped_column(primary_key=True)
    appoint_id = mapped_column(ForeignKey("appointment.id"))
    author_id = mapped_column(ForeignKey("user.id"))
    at: Mapped[datetime.datetime]
    edited_at: Mapped[Optional[datetime.datetime]]
    deleted: Mapped[bool] = mapped_column(default = False)

class Language(db_base.Model):
    __tablename__ = "language"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Mf_recovery_code(db_base.Model):
    __tablename__ = "mf_recovery_code"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates = "mf_recovery_codes")

class Notification_type(db_base.Model):
    __tablename__ = "notification_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Payment(db_base.Model):
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

class Payment_method(db_base.Model):
    __tablename__ = "payment_method"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Payment_status(db_base.Model):
    __tablename__ = "payment_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Payment_type(db_base.Model):
    __tablename__ = "payment_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Role(db_base.Model, fsqla.FsRoleMixin):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Service(db_base.Model):
    __tablename__ = "service"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str] = mapped_column(default = "")

class Service_role(db_base.Model):
    __tablename__ = "service_role"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int]
    role_id: Mapped[int]

class Slot(db_base.Model):
    __tablename__ = "slot"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime.datetime]
    opened: Mapped[bool]
    opened_by_id = mapped_column(ForeignKey("user.id", use_alter=True), nullable=True)
    open_by = relationship("User", foreign_keys=[opened_by_id])
    opened_at: Mapped[datetime.datetime]
    occupied: Mapped[bool]
    occupied_by_appoint_id = mapped_column(ForeignKey("appointment.id", use_alter=True), nullable=True)
    occupied_by_appoint = relationship("Appointment", foreign_keys=[occupied_by_appoint_id])

class User(db_base.Model, fsqla.FsUserMixin):
    _tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique = True)
    password: Mapped[Optional[str]]
    active: Mapped[str] = mapped_column(default = True)
    # fs_uniquifier: Mapped[str] = mapped_column(unique = True) 
    confirmed_at: Mapped[Optional[datetime.datetime]]
    last_login_at: Mapped[Optional[datetime.datetime]]
    current_login_at: Mapped[Optional[datetime.datetime]]
    last_login_ip: Mapped[Optional[str]] 
    current_login_ip: Mapped[Optional[str]] 
    login_count: Mapped[int] 
    # mf_recovery_codes: Mapped[List["Mf_recovery_code"]] = relationship(back_populates = "user")
    name: Mapped[str]   
    instagram: Mapped[str] 
    tel: Mapped[Optional[str]]
    language_id = mapped_column(ForeignKey("language.id"), nullable=True)
    language = relationship("Language", foreign_keys=[language_id]) 
    internal_description: Mapped[Optional[str]]  
    picture_path: Mapped[Optional[str]] = mapped_column(unique = True) 
    # appointment_id: Mapped[List[int]] = relationship(List[])
    # appointment: Mapped[List["Appointment"]] = relationship(back_populates = "user", foreign_keys=[appointment_id])
    # role: Mapped[List["User_role"]] = relationship(back_populates = "user")
    lust_update_at: Mapped[datetime.datetime] 
    lust_update_by_id = mapped_column(ForeignKey("user.id"))
    lust_update_by = relationship("User", foreign_keys=[lust_update_by_id])
    deleted: Mapped[bool] = mapped_column(default = False)
    deleted_at: Mapped[Optional[datetime.datetime]]
    deleted_by_id = mapped_column(ForeignKey("user.id"))
    deleted_by = relationship("User", foreign_keys=[deleted_by_id])

class User_notification(db_base.Model):
    __tablename__ = "user_notification"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    type_id = mapped_column(ForeignKey("notification_type.id"))

class User_role(db_base.Model):
    __tablename__ = "user_role"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    role_id = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(foreign_keys=[role_id])
    set_by_id = mapped_column(ForeignKey("user.id"))
    set_by: Mapped["User"] = relationship(foreign_keys=[set_by_id])
    set_at: Mapped[datetime.datetime]


