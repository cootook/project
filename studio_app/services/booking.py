import datetime
import json

from ..db_classes import Appointment, Slot, User
from ..config import Config
from random import randrange
from ..services.user import User_service
from ..services.verification import SMS_Verification

class Booking:
    def __init__(self, datetime: datetime.datetime, slot_id, message: str, client_phone: str, client_name: str, list_of_services: list):
        self.datetime = datetime
        self.date = self.datetime.date()
        self.time = self.datetime.time()
        self.slot_id = slot_id
        self.message = message
        self.client_phone = client_phone
        self.client_name = client_name
        self.client_id = User.get_or_create_id_by_phone(self.client_phone, self.client_name)
        self.client_is_logged_in = User_service.login_by_id(self.client_id)
        self.is_slot_open = Slot.is_open(self.slot_id, self.date, self.time)
        self.list_of_services = list_of_services
        self.appointment_id = Appointment.create(
            self.client_id, 
            json.dumps(self.list_of_services), 
            self.datetime, 
            slot_id, 
            self.message
            ).id
        self.confirmation_code = Appointment.get_by_id(self.appointment_id).sms_confirmation_code
        self.is_phone_verified = False
        
    def is_phone_successfully_verified(self):
        self.is_phone_verified = SMS_Verification.does_code_match_appointment_code()
        if self.is_phone_verified:
            Appointment.set_phone_confirmed(self.appointment_id)
            return True
        else:
            return False 


        


