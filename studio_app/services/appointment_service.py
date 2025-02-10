import datetime
import json

from ..repositories.appointment_repository import AppointmentRepository
from ..repositories.user_repository import UserRepository
from ..models.appointment import AppointmentModel
from random import randrange
from typing import List, Dict
from copy import deepcopy


DEFAULT_CLIENT = {
    "name": "Unknown Client",
    "tel": "No Phone",
    "description": "No Information Available"
}

class AppointmentService():
    def __init__(self, appointment: AppointmentModel=None):
        self.appointment = appointment
        self.appointment_repo = AppointmentRepository()
        self.user_repo = UserRepository()

    def generate_and_set_confirmation_code(self) -> int: 
        try:
            sms_confirmation_code = self._generate_confirmation_code()
            self.appointment_repo.update_sms_code(self.appointment, sms_confirmation_code)
            return sms_confirmation_code
        except Exception as e:
            self._log_error("Failed to set confirmation code", e)
            raise
    
    def _generate_confirmation_code(self) -> int:
        return randrange(1000, 9999, 11)
    
    def get_all_as_list(self) -> List[Dict]:
        try:
            all_appointments = self.appointment_repo.get_all()
            processed_appointments  = []
            for appointment in all_appointments:
                appointment_data = self._process_appointment(appointment)
                processed_appointments.append(appointment_data)

            return processed_appointments
        except Exception as e:
            self._log_error("Failed to get appointments list", e)
            raise

    def _process_appointment(self, appointment) -> Dict:
        """Process single appointment and add client information"""
        appointment_data = deepcopy(appointment.__dict__)
        appointment_data.pop('_sa_instance_state', None)
        
        try:
            appointment_data["service"] = json.loads(appointment_data["service"])
        except json.JSONDecodeError:
            appointment_data["service"] = {}
            self._log_error(f"Invalid service JSON for appointment {appointment.id}")

        client = self._get_client_info(appointment.user_id)
        appointment_data.update(client)
        
        return appointment_data

    def _get_client_info(self, user_id: int) -> Dict:
        """Get client information, return defaults if not found"""
        client = self.user_repo.get_user_by_id(user_id)
        if client is None:
            return {
                "client_name": DEFAULT_CLIENT["name"],
                "client_tel": DEFAULT_CLIENT["tel"],
                "client_description": DEFAULT_CLIENT["description"]
            }
        
        return {
            "client_name": client.name,
            "client_tel": client.tel,
            "client_description": client.internal_description
        }

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