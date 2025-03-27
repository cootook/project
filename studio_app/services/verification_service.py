from .sms_service import SmsService
from ..config import Config

class SmsVerificationOfBooking:
    def __init__(self, booking):
        self.booking = booking
            
    def verify_code(self, code):
        """
        bypassed until SmsService service launched by Twilio
        """
        if True: #int(self.booking.confirmation_code) == int(code):
            self.booking.set_phone_confirmed()
            return True
        else:
            return False
    
    def send_code(self):
        text = f"{Config.TWILIO_SMS_HEADER}your code: {self.booking.confirmation_code} {Config.TWILIO_SMS_FOOTER}"
        new_sms = SmsService(self.booking.client_phone, text).send()
        return new_sms
    
class SmsVerification:
    def __init__(self,phone: str, code: int):
        self.code = code
        self.phone = phone
    
    def send_code(self):
        text = f"{Config.TWILIO_SMS_HEADER}your code: {self.code} {Config.TWILIO_SMS_FOOTER}"
        new_sms = SmsService(self.phone, text).send()
        return new_sms