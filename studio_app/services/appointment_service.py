from ..repositories.appointment_repository import AppointmentRepository
from ..models.appointment import AppointmentModel
from random import randrange

class AppointmentService():
    def __init__(self, appointment: AppointmentModel):
        self.appointment = appointment
        self.appointment_repo = AppointmentRepository()

    def set_get_confirmation_code_to_appointment(self) -> int:
        sms_confirmation_code = randrange(1000, 9999, 11)
        self.appointment_repo.update_sms_code(self.appointment, sms_confirmation_code)
        return sms_confirmation_code