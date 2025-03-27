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
            description=description
        )
        self.db.add(new_appointment)
        self.db.commit()
        print("# create_appointment ", new_appointment)
        print("# try to find ", self.db.scalar(
            select(AppointmentModel).where(AppointmentModel.id == new_appointment.id)
        ))

        return new_appointment
    
    def get_by_id(self, id) -> AppointmentModel | None:
        return self.db.scalar(
            select(AppointmentModel).where(AppointmentModel.id == id)
        )
    
    def update_sms_code(self, appointment: AppointmentModel, code: int):
        self.db.execute(
            update(AppointmentModel)
            .where(AppointmentModel.id == appointment.id)
            .values(sms_confirmation_code=code)
        )
        self.db.commit()
    
    def set_phone_confirmed(self, appointment: AppointmentModel):
        self.db.execute(
            update(AppointmentModel)
            .where(AppointmentModel.id == appointment.id)
            .values(phone_confirmed=True)
        )
        self.db.commit()

    def get_all(self, page: int = 1, per_page: int = 50) -> List[AppointmentModel]:
        offset = (page - 1) * per_page
        stmt = (
            select(AppointmentModel)
            .order_by(AppointmentModel.at)
            .offset(offset)
            .limit(per_page)
        )
        return self.db.execute(stmt).scalars().all()
    
    def get_count(self) -> int:
        return self.db.scalar(select(func.count()).select_from(AppointmentModel))
        
    def get_description(self, appointment_id: int, user_id: int) -> str:
        result = self.db.scalar(select(AppointmentModel.description)
                    .where(
                        AppointmentModel.id == appointment_id, 
                        AppointmentModel.user_id == user_id
                        )
                        )
        return result or ""
        
    def update_description(self, appointment_id: int, description: int, updated_by_id: int):
        self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment_id).values(
            description = description,
            last_update_at = datetime.datetime.now(),
            last_update_by_id = updated_by_id,
            )
        )
        self.db.commit()

    def set_canceled(self, appointment_id: int, updated_by_id: int):
        self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment_id).values(
            canceled_at = datetime.datetime.now(),
            canceled_by_id = updated_by_id,
            canceled = True,
            last_update_at = datetime.datetime.now(),
            last_update_by_id = updated_by_id,
            )
        )
        self.db.commit()

    def set_confirmed(self, appointment_id: int, confirmed_by_id: int):
        self.db.execute(update(AppointmentModel).where(AppointmentModel.id == appointment_id).values(
            approved_at = datetime.datetime.now(),
            approved_by_id = confirmed_by_id,
            approved = True,
            last_update_at = datetime.datetime.now(),
            last_update_by_id = confirmed_by_id,
            )
        )
        self.db.commit()

    def set_done(
            self, 
            appointment_id: int, 
            set_done_by_id: int, 
            ):
        self.db.execute(
            update(AppointmentModel)
            .where(AppointmentModel.id == appointment_id)
            .values(
                done_at = datetime.datetime.now(),
                done_by_id = set_done_by_id,
                done = True,
                last_update_at = datetime.datetime.now(),
                last_update_by_id = set_done_by_id,
                )
        )
        self.db.commit()

    def set_price(
            self, 
            appointment_id: int, 
            set_by_id: int, 
            price: float
            ):
        self.db.execute(
            update(AppointmentModel)
            .where(AppointmentModel.id == appointment_id)
            .values(
                last_update_at = datetime.datetime.now(),
                last_update_by_id = set_by_id,
                price = price
                )
        )
        self.db.commit()

