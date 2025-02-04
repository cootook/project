import datetime

from ..models.slot import SlotModel
from ..models.appointment import AppointmentModel
from .base_repository import BaseRepository
from sqlalchemy import select, update


class SlotRepository(BaseRepository):
    def get_by_id(self, slot_id) -> SlotModel:
        return self.db.scalar(select(SlotModel).where(SlotModel.id == slot_id))


    def is_open(self, slot: SlotModel, date: datetime.date, time: datetime.time) -> bool:
        slot = SlotModel.query.filter(SlotModel.id == slot.id, SlotModel.date == date, SlotModel.time == time, SlotModel.opened == True).first()  
        return False if slot is None else True 


    def set_booked(self, slot: SlotModel, appointment: AppointmentModel):
        self.db.execute(update(SlotModel).where(SlotModel.id == slot.id).values(opened = False, occupied = True, occupied_by_appoint_id = appointment.id))
        self.db.commit()


    def delete_old_empty(self):
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
        self.db.commit()


    def create_n_days_upfront(self):
        """
        this should be called via
        with app.app_context():
        
        before creating slots the func checks if slots already exist at current day
        if there are any slots the day will be skipped
        """
        print("     # create slots ", self.config.HOW_FAR_IN_FUTURE_CREATE_SLOTS, " days upfront:")
        print("         -- starting from ", datetime.datetime.now())
        time_delta_slots_minutes = self.config.TIME_DELTA_SLOTS_MINUTES 
        service_timedelta = datetime.timedelta(minutes=time_delta_slots_minutes)
        starting_time = datetime.time(self.config.OPEN_AT_TIME_HOUR, self.config.OPEN_AT_TIME_MINUTE)
        ending_time = datetime.time(self.config.OPEN_AT_TIME_HOUR, self.config.OPEN_AT_TIME_MINUTE)
        count_slots_created = 0
        
        count_for_cycle = self.config.HOW_FAR_IN_FUTURE_CREATE_SLOTS + 1
        for x in reversed(range(self.config.HOW_FAR_IN_FUTURE_CREATE_SLOTS + 1)):
            count_for_cycle = count_for_cycle - 1
            date_to_create_slots = datetime.date.today() + datetime.timedelta(days=x)
            stmt_to_check_slots_at_that_day = SlotModel.query.filter(SlotModel.date == date_to_create_slots)
            slots_of_that_day = self.db.execute(stmt_to_check_slots_at_that_day).all()

            if len(slots_of_that_day) == 0:
                temp_time = starting_time
                while temp_time <= ending_time:
                    new_slot = SlotModel(date=date_to_create_slots, time=temp_time)
                    temp_time = (datetime.datetime.combine(datetime.date(1, 1, 1), temp_time) + service_timedelta).time()
                    self.db.add(new_slot)
                    self.db.commit()
                    count_slots_created = count_slots_created + 1
            elif len(slots_of_that_day) != 0 and count_for_cycle != 0:
                print("         creating new slots stopped where slots exist")
                print("         count created slots: ", count_slots_created)
                break
            else:
                print("         creating new slots finished")
                print("         count created slots: ", count_slots_created)


    def create(self, year: int, month: int, day: int, hour: int, minute: int, is_open = False) -> SlotModel | None:
        """
        this should be called via
        with app.app_context():
        """
        slot = SlotModel(
            date=datetime.date(year, month, day), 
            time=datetime.time(hour, minute), 
            opened = is_open)
        self.db.add(slot)
        self.db.commit()

        return self.db.scalar(
            select(SlotModel).where(
                SlotModel.date == slot.date, 
                SlotModel.time == slot.time)
            )
 

