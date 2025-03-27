from ..config import Config
from twilio.rest import Client
class SmsService:
    def __init__(self, to: str, text: str):
            self.to = to
            self.text = text

    def send(self):
        account_sid = Config.TWILIO_ACCOUNT_SID
        auth_token = Config.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        new_key = client.new_keys.create(friendly_name="sms")
        message = client.messages.create(
            body=self.text,
            from_=Config.TWILIO_FROM_NUMBER,
            to=self.to,
            )
        return message