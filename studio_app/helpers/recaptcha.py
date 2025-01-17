import json
import requests

from ..config import Config

class Recaptcha:
    def __init__(self):
        pass

    def validate (token: str):
        try:
            url = Config.URL_RECAPTCHA
            params = {
            "secret": Config.SECRET_RECAPTCHA,
            "response": token
            }

            recaptcha = requests.post(url, params)
            recaptcha_respond_dict = json.loads(recaptcha.text)

            return True if recaptcha_respond_dict['success'] else False

        except Exception as er:
            print("#helpers.recaptcha.Recaptcha.validate ---recaptcha request")
            print(er)
            return  False