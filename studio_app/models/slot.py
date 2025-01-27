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

    @staticmethod
    def get_by_id(slot_id):
        return db_base.session.scalar(select(SlotModel).where(SlotModel.id == slot_id))

    @staticmethod
    def is_open(slot_id, date: datetime.date, time: datetime.time):
        slot = SlotModel.query.filter(SlotModel.id == slot_id, SlotModel.date == date, SlotModel.time == time, SlotModel.opened == True).first()  
        return False if slot is None else True 

    @staticmethod
    def set_booked(slot_id, appointment_id):
        db_base.session.execute(update(SlotModel).where(SlotModel.id == slot_id).values(opened = False, occupied = True, occupied_by_appoint_id = appointment_id))
        db_base.session.commit()

    @staticmethod
    def delete_old_empty():
        """
        this should be called via
        with app.app_context():
        """
        date_to_delete_slots_before = datetime.date.today() - datetime.timedelta(days=1)
        stmt_old_slots = SlotModel.query.filter(SlotModel.date < date_to_delete_slots_before, SlotModel.occupied == None, SlotModel.opened == False)

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
            stmt_to_check_slots_at_that_day = SlotModel.query.filter(SlotModel.date == date_to_create_slots)
            slots_of_that_day = db_base.session.execute(stmt_to_check_slots_at_that_day).all()

            if len(slots_of_that_day) == 0:
                temp_time = starting_time
                while temp_time <= ending_time:
                    new_slot = SlotModel(date=date_to_create_slots, time=temp_time)
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
        slot = SlotModel(date=date, time=time, opened = is_open)
        db_base.session.add_all([slot,])
        db_base.session.commit()
        new_slot = SlotModel.query.filter(SlotModel.date == date, SlotModel.time == time).first()
        if new_slot == None:
            print("creating failed")
        else:
            print("created slot id: ", new_slot.id)
