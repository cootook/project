import datetime

from ..models.slot import SlotModel
from ..models.base import db_base
from ..config import Config


def seed_slots(days_seed_upfront=Config.HOW_FAR_IN_FUTURE_CREATE_SLOTS):
        """
        this should be called via
        with app.app_context():
        
        before creating slots the func checks if slots already exist at current day
        if there are any slots the day will be skipped
        """
        print("     # create slots ", days_seed_upfront, " days upfront:")
        print("         -- starting from ", datetime.datetime.now())
        service_timedelta = datetime.timedelta(minutes=Config.TIME_DELTA_SLOTS_MINUTES)
        starting_time = datetime.time(Config.OPEN_AT_TIME_HOUR, Config.OPEN_AT_TIME_MINUTE)
        ending_time = datetime.time(Config.CLOSE_AT_TIME_HOUR, Config.CLOSE_AT_TIME_MINUTE)
        count_slots_created = 0
        
        count_for_cycle = days_seed_upfront + 1
        for day in reversed(range(days_seed_upfront + 1)):
            count_for_cycle = count_for_cycle - 1
            date_to_create_slots = datetime.date.today() + datetime.timedelta(days=day)
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