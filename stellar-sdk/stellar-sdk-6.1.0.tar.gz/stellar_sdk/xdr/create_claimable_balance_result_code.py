# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError
from ..type_checked import type_checked

__all__ = ["CreateClaimableBalanceResultCode"]


@type_checked
class CreateClaimableBalanceResultCode(IntEnum):
    """
    XDR Source Code::

        enum CreateClaimableBalanceResultCode
        {
            CREATE_CLAIMABLE_BALANCE_SUCCESS = 0,
            CREATE_CLAIMABLE_BALANCE_MALFORMED = -1,
            CREATE_CLAIMABLE_BALANCE_LOW_RESERVE = -2,
            CREATE_CLAIMABLE_BALANCE_NO_TRUST = -3,
            CREATE_CLAIMABLE_BALANCE_NOT_AUTHORIZED = -4,
            CREATE_CLAIMABLE_BALANCE_UNDERFUNDED = -5
        };
    """

    CREATE_CLAIMABLE_BALANCE_SUCCESS = 0
    CREATE_CLAIMABLE_BALANCE_MALFORMED = -1
    CREATE_CLAIMABLE_BALANCE_LOW_RESERVE = -2
    CREATE_CLAIMABLE_BALANCE_NO_TRUST = -3
    CREATE_CLAIMABLE_BALANCE_NOT_AUTHORIZED = -4
    CREATE_CLAIMABLE_BALANCE_UNDERFUNDED = -5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "CreateClaimableBalanceResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "CreateClaimableBalanceResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "CreateClaimableBalanceResultCode":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )
