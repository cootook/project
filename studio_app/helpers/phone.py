import phonenumbers

from ..config import Config

class Phone:
    def __init__(self, number: str):
        self.parsed = phonenumbers.parse(number, None)
        self.is_valid = phonenumbers.is_valid_number(self.parsed)
        self.canonical = phonenumbers.format_number(self.parsed, phonenumbers.PhoneNumberFormat.E164)
