import datetime
import json

from ..models.appointment import AppointmentModel
from ..models.slot import SlotModel
from ..models.user import UserModel
from ..repositories.appointment_repository import AppointmentRepository
from ..repositories.slot_repository import SlotRepository
from ..repositories.user_repository import UserRepository
from random import randrange
from .user_service import UserService
from ..services.appointment_service import AppointmentService



class Booking:
    def __init__(
            self, 
            datetime: datetime.datetime, 
            slot_id: int | str, 
            message: str, 
            client_phone: str, 
            client_name: str, 
            list_of_services: list,
            appointment_id=None):
        self.slot_repo = SlotRepository()
        self.user_repo = UserRepository()
        self.appointment_repo = AppointmentRepository()
        self.datetime = datetime
        self.date = self.datetime.date()
        self.time = self.datetime.time()
        self.slot = self.slot_repo.get_by_id(slot_id)
        self.message = message
        self.client_phone = client_phone
        self.client_name = client_name
        self.client = UserRepository.get_or_create_and_update_user_by_phone(self.client_phone) #set name for client
        self.user_repo.update_user_data(name=client_name)
        self.client_is_logged_in = UserService.login_by_id(self.client_id)
        self.is_slot_open = self.slot_repo.is_open(self.slot, self.date, self.time)
        self.list_of_services = list_of_services
        self.appointment_id = appointment_id or self.appointment_repo.create(
            user_id=self.client.id, 
            service=json.dumps(self.list_of_services), 
            at=self.datetime, 
            slot_id=self.slot.id,
            last_update_by_id=self.client.id,
            description=message,
        ).id
        self.confirmation_code = self.appointment_service.generate_and_set_confirmation_code()
        self.is_phone_verified = False
        self.appointment_service = AppointmentService(self.appointment_repo.get_by_id(self.appointment_id))
        
    def set_phone_confirmed(self):
        self.appointment_repo.set_phone_confirmed(self.appointment)
    
    def to_json(self):
        data = self.__dict__.copy()
        data['datetime'] = self.datetime.isoformat()  
        data['date'] = self.date.isoformat() 
        data['time'] = self.time.isoformat()
        return json.dumps(data)
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        data['datetime'] = datetime.datetime.fromisoformat(data['datetime'])
        return cls(
            datetime=data['datetime'],
            slot_id=data['slot_id'],
            message=data['message'],
            client_phone=data['client_phone'],
            client_name=data['client_name'],
            list_of_services=data['list_of_services'],
            appointment_id=data['appointment_id']
        )

    def reserve_slot(self):
        self.slot_repo.set_booked(
            self.slot,
            self.appointment_repo.get_by_id(self.appointment_id)
        )
