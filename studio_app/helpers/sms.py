import json
from ..config import Config
from twilio.rest import Client
class SMS:
    def __init__(self):
            pass
    @staticmethod
    def send(to_number, sms_text):
        account_sid = Config.TWILIO_ACCOUNT_SID
        auth_token = Config.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        new_key = client.new_keys.create(friendly_name="sms")
        message = client.messages.create(
            body=sms_text,
            from_=Config.TWILIO_FROM_NUMBER,
            to=to_number,
            )
        return json.dumps(message)