import requests
from . import security
from .types import TeleBirrData
from django.conf import settings

URL = settings.TELEBIRR_URL


class TeleBirrRequester:
    def __init__(self, data: TeleBirrData) -> None:
        self.data = data

    def create_transaction(self):
        encrypter = security.Encrypter(vars(self.data))

        request_data = {
            'appid': self.data.appId,
            'sign': encrypter.get_signature(),
            'ussd': encrypter.encrypt()
        }

        result = requests.request(
            'POST',
            URL,
            json=request_data
        )
        return result.json()
