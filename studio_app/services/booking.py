import datetime
import json

from ..db_classes import Appointment, Slot, User
from random import randrange
from ..services.user import UserService

class Booking:
    def __init__(self, datetime: datetime.datetime, slot_id, message: str, client_phone: str, client_name: str, list_of_services: list, appointment_id = None):
        self.datetime = datetime
        self.date = self.datetime.date()
        self.time = self.datetime.time()
        self.slot_id = slot_id
        self.message = message
        self.client_phone = client_phone
        self.client_name = client_name
        self.client_id = User.get_or_create_id_by_phone(self.client_phone, self.client_name)
        self.client_is_logged_in = UserService.login_by_id(self.client_id)
        self.is_slot_open = Slot.is_open(self.slot_id, self.date, self.time)
        self.list_of_services = list_of_services
        self.appointment_id = appointment_id or Appointment.create(
                self.client_id, 
                json.dumps(self.list_of_services), 
                self.datetime, 
                self.slot_id, 
                self.message
                ).id
        self.confirmation_code = Appointment.get_by_id(self.appointment_id).sms_confirmation_code
        self.is_phone_verified = False
        
    def set_phone_confirmed(self):
        Appointment.set_phone_confirmed(self.appointment_id)
    
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
        Slot.set_booked(self.slot_id, self.appointment_id)