import datetime
import os
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

    def create(user_id, service, date_time, slot_id, description):
        # define service id
        """
        this should be called via
        with app.app_context():
        """
        new_appointment = Appointment(user_id=user_id, service_id = 1, at=date_time, slot_id=slot_id, description=description )
        db_base.session.add(new_appointment)
        db_base.session.commit()
        return new_appointment

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

# class Mf_recovery_code(db_base.Model):
#     __tablename__ = "mf_recovery_code"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(unique = True)
#     description: Mapped[str] = mapped_column(default = "")
#     user_id = mapped_column(ForeignKey("user.id"))
#     user: Mapped["User"] = relationship(back_populates = "mf_recovery_codes")

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

    def create(name, description):
        new_service = Service(name=name, description=description)
        db_base.session.add(new_service)
        db_base.session.commit()
        return new_service

class Service_role(db_base.Model):
    __tablename__ = "service_role"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int]
    role_id: Mapped[int]

class Slot(db_base.Model):
    __tablename__ = "slot"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date]
    time: Mapped[datetime.time]
    opened: Mapped[bool] = mapped_column(default = False)
    opened_by_id = mapped_column(ForeignKey("user.id", use_alter=True), nullable=True)
    open_by = relationship("User", foreign_keys=[opened_by_id])
    opened_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    occupied: Mapped[bool] = mapped_column(nullable=True)
    occupied_by_appoint_id = mapped_column(ForeignKey("appointment.id", use_alter=True), nullable=True)
    occupied_by_appoint = relationship("Appointment", foreign_keys=[occupied_by_appoint_id])
    # owned_by_id = mapped_column(ForeignKey("user.id", use_alter=True), nullable=True)
    # owned_by = relationship("User", foreign_keys=[opened_by_id])

    def book(for_user_id, requested_slot, appointment):
        requested_slot.opened = False
        requested_slot.occupied = True
        requested_slot.occupied_by_appoint_id = appointment.id
        db_base.session.commit()
        return True

    def delete_old_empty():
        """
        this should be called via
        with app.app_context():
        """
        date_to_delete_slots_before = datetime.date.today() - datetime.timedelta(days=1)
        stmt_old_slots = Slot.query.filter(Slot.date < date_to_delete_slots_before, Slot.occupied == None, Slot.opened == False)

        print("     # delete old empty slots:")
        if len(stmt_old_slots.all()) == 0:
            print("         -- nothing to delete")
        else:
            print("         -- deleting ", len(stmt_old_slots.all()), " slots")
        for slot in stmt_old_slots.all():
            print("         ", "id:", slot.id, ", date:", slot.date, ", time:", slot.time)
        
        stmt_old_slots.delete()
        db_base.session.commit()

    def create_n_days_upfront(how_many_days_for_advance_to_populate_slot_table = int(os.environ.get("HOW_FAR_IN_FUTURE_CREATE_SLOTS"))):
        """
        this should be called via
        with app.app_context():
        
        before creating slots the func checks if slots already exist at current day
        if there are any slots the day will be skipped
        """
        print("     # create slots ", how_many_days_for_advance_to_populate_slot_table, " days upfront:")
        print("         -- starting from ", datetime.datetime.now())
        time_delta_slots_minutes = int(os.environ.get("TIME_DELTA_SLOTS_MINUTES"))
        service_timedelta = datetime.timedelta(minutes=time_delta_slots_minutes)
        starting_time = datetime.time(int(os.environ.get("OPEN_AT_TIME_HOUR")), int(os.environ.get("OPEN_AT_TIME_MINUTE")))
        ending_time = datetime.time(int(os.environ.get("CLOSE_AT_TIME_HOUR")), int(os.environ.get("CLOSE_AT_TIME_MINUTE")))
        count_slots_created = 0
        
        count_for_cycle = how_many_days_for_advance_to_populate_slot_table + 1
        for x in reversed(range(how_many_days_for_advance_to_populate_slot_table + 1)):
            count_for_cycle = count_for_cycle - 1
            date_to_create_slots = datetime.date.today() + datetime.timedelta(days=x)
            stmt_to_check_slots_at_that_day = Slot.query.filter(Slot.date == date_to_create_slots)
            slots_of_that_day = db_base.session.execute(stmt_to_check_slots_at_that_day).all()

            if len(slots_of_that_day) == 0:
                temp_time = starting_time
                while temp_time <= ending_time:
                    new_slot = Slot(date=date_to_create_slots, time=temp_time)
                    temp_time = (datetime.datetime.combine(datetime.date(1, 1, 1), temp_time) + service_timedelta).time()
                    db_base.session.add(new_slot)
                    db_base.session.commit()
                    count_slots_created = count_slots_created + 1
            elif len(slots_of_that_day) != 0 and count_for_cycle != 0:
                print("         creating new slots stopped where slots exist")
                print("         count created slots: ", count_slots_created)
                break
            else:
                print("         creating new slots finished")
                print("         count created slots: ", count_slots_created)

    def create(year: int, month: int, day: int, hour: int, minute: int, is_open = False):
        """
        this should be called via
        with app.app_context():
        """
        date = datetime.date(year, month, day)
        time = datetime.time(hour, minute)
        slot = Slot(date=date, time=time, opened = is_open)
        db_base.session.add_all([slot,])
        db_base.session.commit()
        new_slot = Slot.query.filter(Slot.date == date, Slot.time == time).first()
        if new_slot == None:
            print("creating failed")
        else:
            print("created slot id: ", new_slot.id)
    
  

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
    lust_update_at: Mapped[Optional[datetime.datetime]] 
    lust_update_by_id = mapped_column(ForeignKey("user.id"), nullable=True)
    lust_update_by = relationship("User", foreign_keys=[lust_update_by_id])
    deleted: Mapped[bool] = mapped_column(default = False)
    deleted_at: Mapped[Optional[datetime.datetime]]
    deleted_by_id = mapped_column(ForeignKey("user.id"), nullable=True)
    deleted_by = relationship("User", foreign_keys=[deleted_by_id])

# #### USE CLASS USER_AS_WORKER WHEN MORE THAN ONE WORKER, UPDATE SLOT GENERATION 

# class User_as_worker(db_base.Model):
#     __tablename__ = "user_as_worker"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id = mapped_column(ForeignKey("user.id"))
#     time_slot_duration_minutes: Mapped[Optional[int]]
#     qualification: Mapped[Optional[str]]
#     description: Mapped[Optional[str]]
#     created_at: Mapped[Optional[datetime.datetime]] 
#     created_by_id = mapped_column(ForeignKey("user.id"), nullable=True)
#     created_by = relationship("User", foreign_keys=[created_by_id])
#     lust_update_at: Mapped[Optional[datetime.datetime]] 
#     lust_update_by_id = mapped_column(ForeignKey("user.id"), nullable=True)
#     lust_update_by = relationship("User", foreign_keys=[lust_update_by_id])
#     deleted: Mapped[bool] = mapped_column(default = False)
#     deleted_at: Mapped[Optional[datetime.datetime]]
#     deleted_by_id = mapped_column(ForeignKey("user.id"), nullable=True)
#     deleted_by = relationship("User", foreign_keys=[deleted_by_id])

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


