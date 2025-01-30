from ..models.role import Role
from ..models.base import db

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