import datetime

from ..models.slot import SlotModel
from ..models.base import data_base
from ..config import Config
from flask_sqlalchemy import SQLAlchemy


def seed_slots(           
          db_session: SQLAlchemy=data_base, 
          config=Config
          ):
        """
        before creating slots the func checks if slots already exist at current day
        if there are any slots the day will be skipped
        """
        days_seed_upfront: int=Config.HOW_FAR_IN_FUTURE_CREATE_SLOTS
        print("     # create slots ", days_seed_upfront, " days upfront:")
        print("         -- starting from ", datetime.datetime.now())
        service_timedelta = datetime.timedelta(minutes=config.TIME_DELTA_SLOTS_MINUTES)
        starting_time = datetime.time(config.OPEN_AT_TIME_HOUR, config.OPEN_AT_TIME_MINUTE)
        ending_time = datetime.time(config.CLOSE_AT_TIME_HOUR, config.CLOSE_AT_TIME_MINUTE)
        count_slots_created = 0
        
        count_for_cycle = days_seed_upfront + 1
        for day in reversed(range(days_seed_upfront + 1)):
            count_for_cycle = count_for_cycle - 1
            date_to_create_slots = datetime.date.today() + datetime.timedelta(days=day)
            stmt_to_check_slots_at_that_day = SlotModel.query.filter(SlotModel.date == date_to_create_slots)
            slots_of_that_day = db_session.session.execute(stmt_to_check_slots_at_that_day).all()

            if len(slots_of_that_day) == 0:
                temp_time = starting_time
                while temp_time <= ending_time:
                    new_slot = SlotModel(date=date_to_create_slots, time=temp_time)
                    temp_time = (datetime.datetime.combine(datetime.date(1, 1, 1), temp_time) + service_timedelta).time()
                    db_session.session.add(new_slot)
                    db_session.session.commit()
                    count_slots_created = count_slots_created + 1
            elif len(slots_of_that_day) != 0 and count_for_cycle != 0:
                print("         creating new slots stopped where slots exist")
                print("         count created slots: ", count_slots_created)
                break
            else:
                print("         creating new slots finished")
                print("         count created slots: ", count_slots_created)