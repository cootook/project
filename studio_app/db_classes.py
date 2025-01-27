import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_security import hash_password
from flask_security.models import fsqla_v3 as fsqla
from random import randrange
from sqlalchemy import ForeignKey, update, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref
from typing import List, Optional
from .config import Config

class Base(DeclarativeBase):
    pass

db_base = SQLAlchemy(model_class=Base)

fsqla.FsModels.set_db_info(db_base)

class Appointment(db_base.Model):
    """
    column 'service' value is list of Service.name as JSON str
    """
    __tablename__ = "appointment"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    service: Mapped[str]
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
    sms_confirmation_code: Mapped[Optional[str]]
    phone_confirmed: Mapped[Optional[bool]] = mapped_column(default = False)
    confirmed_by_client: Mapped[Optional[bool]] = mapped_column(default = False)
    canceled_by_client: Mapped[Optional[bool]] = mapped_column(default = False)

    @staticmethod
    def create(user_id, service, date_time, slot_id, description):
        """
        this should be called via
        with app.app_context():
        """
        new_appointment = Appointment(user_id=user_id, service = service, at=date_time, slot_id=slot_id, description=description )
        db_base.session.add(new_appointment)
        db_base.session.commit()
        Appointment.set_get_confirmation_code(new_appointment.id)
        return new_appointment
    
    @staticmethod
    def get_by_id(id):
        return db_base.session.scalar(select(Appointment).where(Appointment.id == id))

    @staticmethod
    def set_get_confirmation_code(appointment_id):
        sms_confirmation_code = randrange(1000, 9999, 11)
        db_base.session.execute(update(Appointment).where(Appointment.id == appointment_id).values(sms_confirmation_code = sms_confirmation_code))
        db_base.session.commit()
        return sms_confirmation_code
    
    @staticmethod
    def set_phone_confirmed(appointment_id):
        db_base.session.execute(update(Appointment).where(Appointment.id == appointment_id).values(phone_confirmed = True))

class ConsentSms(db_base.Model):
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
    deleted: Mapped[bool] = mapped_column(default = False)

    def create(self, name, description):
        new_service = Service(name=name, description=description)
        db_base.session.add(new_service)
        db_base.session.commit()
        return new_service
    
    def delete(self):
        db_base.session.execute(update(Service).where(Service.id == self.id).values(deleted = True))
        db_base.session.commit()
        return
    
    @staticmethod
    def get_list_of_services_from_dict(data: dict):
        services = []
        for item in data:
            if item == data[item]:
                service = db_base.session.scalar(select(Service).where(Service.name == item, Service.deleted == False))
                if not service is None:
                    services.append(item)
        return services

class Slot(db_base.Model):
    __tablename__ = "slot"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date]
    time: Mapped[datetime.time]
    opened: Mapped[bool] = mapped_column(default = False)
    opened_by_id = mapped_column(ForeignKey("user.id", use_alter=True), nullable=True)
    opened_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
    occupied: Mapped[bool] = mapped_column(nullable=True)
    occupied_by_appoint_id = mapped_column(ForeignKey("appointment.id", use_alter=True), nullable=True)

    @staticmethod
    def get_by_id(slot_id):
        return db_base.session.scalar(select(Slot).where(Slot.id == slot_id))

    @staticmethod
    def is_open(slot_id, date: datetime.date, time: datetime.time):
        slot = Slot.query.filter(Slot.id == slot_id, Slot.date == date, Slot.time == time, Slot.opened == True).first()  
        return False if slot is None else True 

    @staticmethod
    def set_booked(slot_id, appointment_id):
        db_base.session.execute(update(Slot).where(Slot.id == slot_id).values(opened = False, occupied = True, occupied_by_appoint_id = appointment_id))
        db_base.session.commit()

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
    email: Mapped[Optional[str]] = mapped_column(unique = True)
    password: Mapped[Optional[str]]
    active: Mapped[str] = mapped_column(default = True)
    confirmed_at: Mapped[Optional[datetime.datetime]]
    last_login_at: Mapped[Optional[datetime.datetime]]
    current_login_at: Mapped[Optional[datetime.datetime]]
    last_login_ip: Mapped[Optional[str]] 
    current_login_ip: Mapped[Optional[str]] 
    login_count: Mapped[int] 
    name: Mapped[Optional[str]]   
    tel: Mapped[Optional[str]]
    internal_description: Mapped[Optional[str]]  
    lust_update_at: Mapped[Optional[datetime.datetime]] 
    lust_update_by_id = mapped_column(ForeignKey("user.id"), nullable=True)
    deleted: Mapped[bool] = mapped_column(default = False)
    deleted_at: Mapped[Optional[datetime.datetime]]
    deleted_by_id = mapped_column(ForeignKey("user.id"), nullable=True)

    @staticmethod
    def get_or_create_id_by_phone(phone: str, name: str):
        """
        the method updates user's name if user with this phone exists
        """
        user = db_base.session.scalar(select(User).where(User.tel == phone))
        from studio_app.webapp import user_datastore
        if user is None:
            user = user_datastore.create_user(
                tel = phone, 
                name = name, 
                email = f"{phone}@{Config.MAIL_DEFAULT_DOMAIN}", 
                password = hash_password(Config.DEFAULT_PASSWORD))
            db_base.session.add(user)
            db_base.session.commit()
            user_datastore.add_role_to_user(user, "client")
        else:
            db_base.session.execute(update(User).where(User.tel == phone).values(name = name))
            user_datastore.add_role_to_user(user, "client")
            db_base.session.commit()
        return user.id
    
    @staticmethod
    def get_user_by_id(id):
        return db_base.session.scalar(select(User).where(User.id == id))
