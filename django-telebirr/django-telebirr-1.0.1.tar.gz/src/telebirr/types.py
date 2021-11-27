import time
from typing import NewType
from .security import Encrypter


class TeleData:
    appId: str
    shortCode: int
    nonce: str
    notifyUrl: str
    outTradeNo: str
    receiveName: str
    returnUrl: str
    subject: str
    timeoutExpress = 300
    timeStamp: int
    totalAmount: float

    def __init__(self,
                 appId: str,
                 shortCode: int,
                 nonce: str,
                 notifyUrl: str,
                 outTradeNo: str,
                 receiveName: str,
                 returnUrl: str,
                 subject: str,
                 totalAmount: float,
                 timeoutExpress=300
                 ):
        self.appId = appId
        self.shortCode = shortCode
        self.nonce = nonce
        self.notifyUrl = notifyUrl
        self.outTradeNo = outTradeNo
        self.receiveName = receiveName
        self.returnUrl = returnUrl
        self.subject = subject
        self.timeStamp = int(time.time())
        self.timeoutExpress = timeoutExpress
        self.totalAmount = totalAmount

    def generate_ussd(self) -> str:
        encrypter = Encrypter(vars(self))
        return encrypter.encrypt()

    def generate_signature(self) -> str:
        encrypter = Encrypter(vars(self))
        return encrypter.get_signature()


TeleBirrData = NewType('TeleBirrData', TeleData)
