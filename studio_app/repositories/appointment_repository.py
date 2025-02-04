from sqlalchemy import select, update
from ..models.appointment import AppointmentModel
from random import randrange
from .base_repository import BaseRepository


class AppointmentRepository(BaseRepository):
    def create(self, **kwargs):
        new_appointment = AppointmentModel(sms_confirmation_code=randrange(1000, 9999, 11), **kwargs)
        self.db.add(new_appointment)
        self.db.commit()
        return new_appointment
    
    def get_by_id(self, id) -> AppointmentModel:
        return self.db.scalar(select(AppointmentModel).where(AppointmentModel.id == id))

    def set_get_confirmation_code(self, appointment: AppointmentModel) -> int:
        sms_confirmation_code = randrange(1000, 9999, 11)
        self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment.id).values(sms_confirmation_code = sms_confirmation_code))
        self.db.commit()
        return sms_confirmation_code
    
    def set_phone_confirmed(self, appointment: AppointmentModel):
        self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment.id).values(phone_confirmed = True))
