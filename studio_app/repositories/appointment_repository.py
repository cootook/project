import datetime

from sqlalchemy import select, update, func
from ..models.appointment import AppointmentModel
from random import randrange
from .base_repository import BaseRepository
from typing import List


class AppointmentRepository(BaseRepository):
    def create(self,
            user_id: int, 
            service: str, 
            at: datetime.datetime, 
            slot_id: int,
            last_update_by_id: int,
            description: str,
            amount_time_min: int = 0,
            price: float = 0
            ) -> AppointmentModel:
        try:
            new_appointment = AppointmentModel(
                sms_confirmation_code=randrange(1000, 9999, 11),
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
        except Exception as e:
            self.db.rollback()
            raise
    
    def get_by_id(self, id) -> AppointmentModel:
        try:
            return self.db.scalar(
                select(AppointmentModel).where(AppointmentModel.id == id)
            )
        except Exception as e:
            self._log_error(f"Failed to get appointment {id}", e)
            return None

    
    def update_sms_code(self, appointment: AppointmentModel, code: int):
        try:
            self.db.execute(
                update(AppointmentModel)
                .where(AppointmentModel.id == appointment.id)
                .values(sms_confirmation_code=code)
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise
    
    def set_phone_confirmed(self, appointment: AppointmentModel):
        try:
            self.db.execute(
                update(AppointmentModel)
                .where(AppointmentModel.id == appointment.id)
                .values(phone_confirmed=True)
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise

    def get_all(self, page: int = 1, per_page: int = 50) -> List[AppointmentModel]:
        try:
            offset = (page - 1) * per_page
            stmt = (
                select(AppointmentModel)
                .order_by(AppointmentModel.at)
                .offset(offset)
                .limit(per_page)
            )
            return self.db.execute(stmt).scalars().all()
        except Exception as e:
            self._log_error("Failed to get appointments", e)
            return []
        
    
    def get_count(self) -> int:
        try:
            return self.db.scalar(select(func.count()).select_from(AppointmentModel))
        except Exception as e:
            self._log_error("Failed to get appointment count", e)
            return 0
        
