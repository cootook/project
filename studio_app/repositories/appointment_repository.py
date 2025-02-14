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
        
    def get_description(self, appointment_id: int, user_id: int) -> str:
        try:
            result = self.db.scalar(select(AppointmentModel.description)
                        .where(
                            AppointmentModel.id == appointment_id, 
                            AppointmentModel.user_id == user_id
                            )
                            )
            return result or ""
        except Exception as e:
            self._log_error("Failed to get description", e)
            return ""
        
    def update_description(self, appointment_id: int, description: int, updated_by_id: int):
        try:
            self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment_id).values(
                description = description,
                last_update_at = datetime.datetime.now(),
                last_update_by_id = updated_by_id,
                )
            )
            self.db.commit()
        except Exception as e:
            self._log_error("Failed to update description", e)
            self.db.rollback()
            raise
    
    def set_canceled(self, appointment_id: int, updated_by_id: int):
        try:
            self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment_id).values(
                canceled_at = datetime.datetime.now(),
                canceled_by_id = updated_by_id,
                canceled = True,
                last_update_at = datetime.datetime.now(),
                last_update_by_id = updated_by_id,
                )
            )
            self.db.commit()
        except Exception as e:
            self._log_error(f"Failed cancel appointment {appointment_id}", e)
            self.db.rollback()
            raise

    def set_confirmed(self, appointment_id: int, confirmed_by_id: int) -> bool:
        try:
            self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment_id).values(
                approved_at = datetime.datetime.now(),
                approved_by_id = confirmed_by_id,
                approved = True,
                last_update_at = datetime.datetime.now(),
                last_update_by_id = confirmed_by_id,
                )
            )
            self.db.commit()
            return True
        
        except Exception as e:
            self._log_error(f"Failed approve appointment {appointment_id}", e)
            self.db.rollback()
            raise
