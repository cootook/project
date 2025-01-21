from ..helpers.sms import SMS
from ..config import Config

class SMS_Verification_of_Booking:
    def __init__(self, booking):
        self.booking = booking
            
    def verify_code(self, code):
        """
        bypassed until SMS service launched by Twilio
        """
        if True: #int(self.booking.confirmation_code) == int(code):
            self.booking.set_phone_confirmed()
            return True
        else:
            return False
    
    def send_code(self):
        text = f"{Config.TWILIO_SMS_HEADER}your code: {self.booking.confirmation_code} {Config.TWILIO_SMS_FOOTER}"
        new_sms = SMS(self.booking.client_phone, text).send()
        return new_sms
    