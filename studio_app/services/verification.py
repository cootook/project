from ..db_classes import Appointment

class SMS_Verification:
    def __init__(self):
        pass
    
    @staticmethod
    def does_code_match_appointment_code(code, appointment_id):
        appointment_verification_code = Appointment.get_by_id(appointment_id).sms_confirmation_code
        return True if int(appointment_verification_code) == int(code) else False