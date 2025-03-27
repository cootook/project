from ..repositories.appointment_repository import AppointmentRepository
from ..repositories.slot_repository import SlotRepository
from ..repositories.user_repository import UserRepository

class SlotService:
    def __init__(self):        
        self.slot_repo = SlotRepository()
        self.user_repo = UserRepository()
        self.appointment_repo = AppointmentRepository()
        

    def reserve_slot(self, slot_id, appointment_id):
        appointment = self.appointment_repo.get_by_id(appointment_id)
        slot = self.slot_repo.get_by_id(slot_id)

        self.slot_repo.set_booked(
                slot,
                appointment
            )