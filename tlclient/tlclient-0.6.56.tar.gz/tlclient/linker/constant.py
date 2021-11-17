# auto generated by update_py.py
import inspect
import typing
import enum
from typing import Dict

FIST_NAME_MAX_LIMIT = 30
FIST_ROUTING_ID_MAX_LIMIT = 64
FIST_ADDR_MAX_LIMIT = 100
MASTER_ERR_MSG_MAX_LIMIT = 50
FRAME_BUFFER_DEFAULT_SIZE = 1000
NOTIFICATION_TITLE_LIMIT = 50
NOTIFICATION_MESSAGE_LIMIT = 200
ANY_FIST_NAME = '*'
DEFAULT_REQ_ID = 0
MASTER_FIST_NAME = 'master'
IS_NEW_VERSION = False


class ReadableEnum(object):
    _code_name_cache = None

    @classmethod
    def init_cache(cls):
        cls._code_name_cache = ({}, {})
        for name in dir(cls):
            attr = getattr(cls, name)
            if name.startswith('_') or inspect.ismethod(attr):
                continue
            # assert attr not in cls._code_name_cache[0], f'failed to register {name}, {attr} is a registed value'
            # assert name not in cls._code_name_cache[1], f'failed to register {attr}, {name} is a registed enum'
            cls._code_name_cache[0][attr] = name
            cls._code_name_cache[1][name] = attr

    @classmethod
    def read(cls, code):
        if cls._code_name_cache is None:
            cls.init_cache()
        return cls._code_name_cache[0].get(code, code)

    @classmethod
    def parse(cls, code):
        if cls._code_name_cache is None:
            cls.init_cache()
        return cls._code_name_cache[1].get(code, code)


class RunnerStatus(ReadableEnum):
    IDLE = 0
    RUNNING = 1
    TO_STOP = 2
    STOPPED = 3


class CommType(ReadableEnum):
    NOT_AVAILABLE = 0
    Zmq = 10
    Zmq_PUB = 11
    Zmq_SUB = 12
    Zmq_REP = 13
    Zmq_REQ = 14
    Zmq_PULL = 15
    Zmq_PUSH = 16
    Yjj = 20


class CommMethod(ReadableEnum):
    NOT_AVAILABLE = 0
    TCP = 1
    IPC = 2
    MMAP = 3
    INPROC = 4


class FistType(ReadableEnum):
    NOT_AVAILABLE = 0
    MASTER = 1
    BASE = 2
    TEST = 3
    CLIENT = 10
    TRADE_ROUTER = 20
    MARKET_ROUTER = 21
    RECORDER = 22
    ORDER_MANAGER = 30
    RISK_MANAGER = 31
    MD_MANAGER = 32
    MD_GENERATOR = 33
    ALGO_SERVER = 34
    BASKET_SERVER = 35
    TRADE_GATEWAY = 40
    MARKET_GATEWAY = 41
    FRONT_END = 50
    PARAM_SERVER = 60


class MsgType(ReadableEnum, enum.IntEnum):
    NO = 0
    YES = 1
    STRING = 2

    TIMER = 100
    GET_STATUS = 101
    PUB_FIST_START = 102

    PUB_FIST_END = 103
    PUB_FIST_SET = 104
    PUB_FIST_REG = 105
    CMD_REQUEST = 106
    CMD_RESPONSE = 107
    FIST_HEART_BEAT = 108
    CMD_SUICIDE = 109

    REQ_FIST_CREATE = 110
    REQ_FIST_SET = 111
    REQ_FIST_REG = 112
    REQ_FIST_INFO = 113
    REQ_NOTIFY = 114

    RSP_FIST_CREATE = 120
    RSP_FIST_SET = 121
    RSP_FIST_REG = 122
    RSP_FIST_INFO = 123
    RSP_NOTIFY = 124

    FIST_ADDR_UPDATE = 130
    ENV_INFO_UPDATE = 131
    GET_FULL_STATUS = 132


class NotificationType(ReadableEnum):
    TRADE = 0
    SYSTEM = 1
    RISK_CONTROL = 2


class HeartBeatStatus(ReadableEnum):
    NOT_AVAILABLE = 0
    HEALTHY = 1
    CONNECTION_ERROR = -1
    INTERNAL_ERROR = -2
    DATABASE_ERROR = -3


class SubscribeTopic(ReadableEnum):
    UNEXPECTED = -1
    NOT_AVAILABLE = 0
    SYSTEM = 1
    REQUEST = 2
    RESPONSE = 3

    @staticmethod
    def get_topic_prefix(topic) -> bytes:
        prefix = ''
        if topic == SubscribeTopic.UNEXPECTED:
            prefix = 'unexpt'
        elif topic == SubscribeTopic.SYSTEM:
            prefix = 'sys'
        elif topic == SubscribeTopic.REQUEST:
            prefix = 'req'
        elif topic == SubscribeTopic.RESPONSE:
            prefix = 'rsp'

        return prefix.encode()

    @staticmethod
    def get_default_topic_set(fist_type: int) -> typing.List[int]:
        # subscribe all by default
        topic_set = [SubscribeTopic.NOT_AVAILABLE]
        if fist_type in [FistType.TRADE_GATEWAY, FistType.MARKET_GATEWAY]:
            topic_set = [SubscribeTopic.UNEXPECTED, SubscribeTopic.SYSTEM, SubscribeTopic.REQUEST]

        return topic_set


class MsgTopicManager:
    topics: Dict[MsgType, SubscribeTopic] = {}

    @staticmethod
    def register_topic(msg_type, topic):
        MsgTopicManager.topics[msg_type] = topic

    @staticmethod
    def get_topic(msg_type):
        return MsgTopicManager.topics.get(msg_type, SubscribeTopic.UNEXPECTED)


def init_msg_topics():
    MsgType.init_cache()
    for mt in MsgType._code_name_cache[0].keys():
        MsgTopicManager.register_topic(mt, SubscribeTopic.SYSTEM)
