import datetime
import json

from ..repositories.appointment_repository import AppointmentRepository
from ..repositories.user_repository import UserRepository
from ..models.appointment import AppointmentModel
from ..models.user import UserModel
from random import randrange
from typing import List, Dict
from copy import deepcopy
from flask_security import current_user


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
    
    def get_all_as_list(self, page: int = 1, per_page: int = 50) -> List[Dict]:
        try:
            total_appointments = self.appointment_repo.get_count()
            appointments = self.appointment_repo.get_all(page, per_page)
            
            processed_appointments = []
            for appointment in appointments:
                appointment_data = self._process_appointment(appointment)
                processed_appointments.append(appointment_data)

            return {
                'appointments': processed_appointments,
                'pagination': {
                    'total': total_appointments,
                    'page': page,
                    'per_page': per_page,
                    'pages': (total_appointments + per_page - 1) // per_page
                }
            }
        except Exception as e:
            self._log_error("Failed to get appointments list", e)
            raise

    def _process_appointment(self, appointment) -> Dict:
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

    def format_appointments_for_frontend(self, appointments_data: Dict) -> str:
        try:
            formatted_appointments = []
            for appointment in appointments_data['appointments']:
                formatted_appointment = self._format_datetime_fields(appointment)
                formatted_appointments.append(formatted_appointment)
            
            return json.dumps({
                'appointments': formatted_appointments,
                'pagination': appointments_data['pagination']
            })
        except Exception as e:
            self._log_error("Failed to format appointments for frontend", e)
            raise
    
    def _format_datetime_fields(self, obj: Dict) -> Dict:
        formatted = obj.copy()
        for key, value in formatted.items():
            if isinstance(value, datetime.datetime):
                formatted[key] = value.strftime('%Y-%m-%dT%H:%M:%S')
            elif isinstance(value, datetime.date):
                formatted[key] = value.strftime("%m/%d/%Y")
            elif isinstance(value, datetime.time):
                formatted[key] = value.strftime("%H:%M")
        return formatted
    
    def _log_error(self, message: str, exception: Exception = None) -> None:
        error_msg = f"Error: {message}"
        if exception:
            error_msg += f" - {str(exception)}"
        print(error_msg)

    def cancel_with_message(
            self, 
            appointment_id: int, 
            user_id: int, 
            message: str, 
            canceled_by_user: UserModel=None
            ):
        
        if canceled_by_user is None:
            canceled_by_user = current_user
            
        try:
            self.appointment = self.appointment_repo.get_by_id(appointment_id)
            
            if not self.appointment:
                self._log_error(f"Appointment {appointment_id} not found")
                return False
            
            is_for_user_id = self.appointment.user_id == user_id

            if is_for_user_id:
                current_description = self.appointment_repo.get_description(self)
                cancel_description = f"{message} | {current_description}"
                self.appointment_repo.update_description(self.appointment.id, cancel_description, canceled_by_user.id)
                self.appointment_repo.set_canceled(self.appointment.id, canceled_by_user.id)
                return True
            else:
                return False
        except Exception as e:
            self._log_error("cancel_with_message: Failed to cancel", e)
            raise

    def confirm_booking(self, appointment_id, user_id, confirmed_by: UserModel=None) -> bool:
        if confirmed_by is None:
            confirmed_by_id = current_user.id 
        else:
            confirmed_by_id = confirmed_by.id

        self.appointment = self.appointment_repo.get_by_id(appointment_id)

        if self.appointment is None:
            self._log_error(f"Appointment {appointment_id} not found")
            return False
        
        is_for_user_id = self.appointment.user_id == user_id

        if not is_for_user_id:
            self._log_error(
                "confirm_booking: Failed to confirm", 
                "appointment {self.appointment.id} does not belong to user {user_id}"
                )
            return False
        
        if self.appointment.done:
            self._log_error(
                "confirm_booking: Failed to confirm", 
                "appointment {self.appointment.id} was done"
                )
            return False

        if self.appointment.canceled:
            self._log_error(
                "confirm_booking: Failed to confirm", 
                "appointment {self.appointment.id} was canceled"
                )
            return False
        
        success = self.appointment_repo.set_confirmed(
            self.appointment.id,
            confirmed_by_id
        )

        return success