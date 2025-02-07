import datetime
import json

from ..repositories.appointment_repository import AppointmentRepository
from ..repositories.user_repository import UserRepository
from ..models.appointment import AppointmentModel
from random import randrange
from typing import List, Dict
from copy import deepcopy


class AppointmentService():
    def __init__(self, appointment: AppointmentModel=None):
        self.appointment = appointment
        self.appointment_repo = AppointmentRepository()
        self.user_repo = UserRepository()

    def set_get_confirmation_code_to_appointment(self) -> int:
        sms_confirmation_code = randrange(1000, 9999, 11)
        self.appointment_repo.update_sms_code(self.appointment, sms_confirmation_code)
        return sms_confirmation_code
    
    def get_all_as_list(self) -> List[Dict]:
        now = datetime.datetime.now()
        all_appointments = self.appointment_repo.get_all()

        user_appointments_for_frontend = []
        list_of_appointments = []
        for appointment in all_appointments:
            temp = deepcopy(appointment.__dict__)
            temp.pop('_sa_instance_state', None)
            temp["service"] = json.loads(temp["service"])
            
            client = self.user_repo.get_user_by_id(appointment.user_id) 
            if client is None:
                temp["client_name"] = "no name"
                temp["client_tel"] = "no phone" 
                temp["client_description"] = "no info"
            else:
                temp["client_name"] = client.name
                temp["client_tel"] = client.tel 
                temp["client_description"] = client.internal_description

            list_of_appointments.append(temp)
        return list_of_appointments

    def get_js_object_out_of_list_of_appointments(self, list_of_appointments: List[Dict]) -> str:
        def convert(obj):
            for el in obj:
                if isinstance(obj[el], datetime.datetime):
                    obj.update({el: obj[el].strftime('%Y-%m-%dT%H:%M:%S')})
                elif isinstance(obj[el], datetime.date):
                    obj.update({el: obj[el].strftime("%m/%d/%Y")})
                elif isinstance(obj[el], datetime.time):
                    obj.update({el: obj[el].strftime("%H:%M")})
            return obj
        list_of_appointments_as_str = []
        for appointment in list_of_appointments:
            appointment_as_str = convert(appointment)
            list_of_appointments_as_str.append(appointment_as_str)
            
        return json.dumps(list_of_appointments_as_str)