from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import json
import hashlib
import base64
from django.conf import settings


class Encrypter:
    def __init__(self, data: dict):
        self.data = data
        self.APP_KEY = settings.TELEBIRR_APP_KEY

    def generate_string(self) -> str:
        self.data['appKey'] = self.APP_KEY
        final_string = ""

        for key in sorted(self.data.keys()):
            if self.data[key] is None or self.data[key] == "":
                continue
            final_string += f'{key}={self.data[key]}&'

        return final_string[:-1]  # removing trailing &

    def get_signature(self) -> str:
        signer = hashlib.new('sha256')
        signer.update(self.generate_string().encode())
        return hashlib.sha256(self.generate_string().encode()).hexdigest()

    def encrypt(self) -> str:
        message = json.dumps(self.data).encode('utf-8')
        public_key = RSA.importKey(open('public.key').read())
        encryptor = PKCS1_v1_5.new(public_key)
        length = 117
        offset = 0
        res = []
        while len(message) - offset > 0:
            if len(message) - offset > length:
                res.append(encryptor.encrypt(message[offset:offset + length]))
            else:
                res.append(encryptor.encrypt(message[offset:]))

            offset += length

        return base64.b64encode(b''.join(res)).decode('utf8')

    # @classmethod
    # def decrypt(cls, data):
    #     NODE_TEMPLATE = Template(
    #         """
    #         const PUB_KEY = "$PUB_KEY"
    #         const NodeRSA = require('node-rsa');
    #         const rsaKey = new NodeRSA(PUB_KEY, "public", { encryptionScheme: "pkcs1" });
    #         const raw = $DATA;
    #         const decryptedData = rsaKey.decryptPublic(raw, "utf8");
    #         process.stdout.write(decryptedData);
    #     """
    #     )
    #
    #     with open('tele-decrypt.js', 'w') as f:
    #         f.write(
    #             NODE_TEMPLATE.substitute({'PUB_KEY': open('public.key').read().replace('\n', ''), 'DATA': data})
    #         )
    #
    #     return eval(os.popen('node tele-decrypt.js').read())


# class TeleBirrRequester:
#     @classmethod
#     def create_transaction(cls, transaction: 'payments.models.TelebirrTransaction'):
#         data = {
#             'appId': APP_ID,
#             'nonce': str(transaction.id),
#             'notifyUrl': config('TELEBIRR_WEBHOOK', None),
#             'outTradeNo': str(transaction.id),
#             'receiveName': transaction.receive_name,
#             'returnUrl': 'https://ashewa.com',
#             'shortCode': SHORT_CODE.__str__(),
#             'subject': transaction.subject or "ashewa payment",
#             'timeoutExpress': '360000',
#             'timestamp': time.time().__int__().__str__(),
#             'totalAmount': transaction.amount,
#         }
#
#         request_data = {
#             'appid': APP_ID,
#             'sign': Signature.get_signature(data),
#             'ussd': UssdEncryption.encrypt(data)
#         }
#
#         result = requests.request(
#             'POST',
#             URL,
#             json=request_data
#         )
#         return result.json()
#
#
#
# class Signature:
#     @classmethod
#     def generate_string(cls, ussd_data) -> str:
#         ussd_data['appKey'] = APP_KEY
#         final_string = ""
#
#         for key in sorted(ussd_data.keys()):
#             if ussd_data[key] is None or ussd_data[key] == "":
#                 continue
#             final_string += f'{key}={ussd_data[key]}&'
#
#         return final_string[:-1]  # removing trailing &
#
#     @classmethod
#     def get_signature(cls, data):
#         signer = hashlib.new('sha256')
#         signer.update(cls.generate_string(data).encode())
#         return hashlib.sha256(cls.generate_string(data).encode()).hexdigest()
#
#
# class UssdEncryption:
#     @classmethod
#     def encrypt(cls, data):
#         message = json.dumps(data).encode('utf-8')
#         public_key = RSA.importKey(open('public.key').read())
#         encryptor = PKCS1_v1_5.new(public_key)
#         length = 117
#         offset = 0
#         res = []
#         while len(message) - offset > 0:
#             if len(message) - offset > length:
#                 res.append(encryptor.encrypt(message[offset:offset + length]))
#             else:
#                 res.append(encryptor.encrypt(message[offset:]))
#
#             offset += length
#
#         return base64.b64encode(b''.join(res)).decode('utf8')
#
#     @classmethod
#     def decrypt(cls, data):
#         NODE_TEMPLATE = Template(
#             """
#             const PUB_KEY = "$PUB_KEY"
#             const NodeRSA = require('node-rsa');
#             const rsaKey = new NodeRSA(PUB_KEY, "public", { encryptionScheme: "pkcs1" });
#             const raw = $DATA;
#             const decryptedData = rsaKey.decryptPublic(raw, "utf8");
#             process.stdout.write(decryptedData);
#         """
#         )
#
#         with open('tele-decrypt.js', 'w') as f:
#             f.write(
#                 NODE_TEMPLATE.substitute({'PUB_KEY': open('public.key').read().replace('\n', ''), 'DATA': data})
#             )
#
#         return eval(os.popen('node tele-decrypt.js').read())
#
#
#
