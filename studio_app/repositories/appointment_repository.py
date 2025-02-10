import datetime

from sqlalchemy import select, update
from ..models.appointment import AppointmentModel
from random import randrange
from .base_repository import BaseRepository
from typing import List


class AppointmentRepository(BaseRepository):
    def create(self,
            user_id, 
            service, 
            at, 
            slot_id,
            last_update_by_id,
            description,
            amount_time_min=0,
            price=0
            ):
        new_appointment = AppointmentModel(
            user_id=user_id, 
            service=service, 
            at=at, 
            price=price,
            slot_id=slot_id,
            amount_time_min=amount_time_min,
            last_update_at=datetime.datetime.now(),
            last_update_by_id=last_update_by_id,
            description=description,
            )
        self.db.add(new_appointment)
        self.db.commit()
        return new_appointment
    
    def get_by_id(self, id) -> AppointmentModel:
        return self.db.scalar(select(AppointmentModel).where(AppointmentModel.id == id))

    
    def update_sms_code(self, appointment: AppointmentModel, code: int):
        self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment.id).values(sms_confirmation_code=code))
    
    def set_phone_confirmed(self, appointment: AppointmentModel):
        self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment.id).values(phone_confirmed = True))

    def get_all(self) -> List[AppointmentModel]:
        stmt = select(AppointmentModel).order_by(AppointmentModel.at)
        result = self.db.execute(stmt).scalars().all()
        return result
        
