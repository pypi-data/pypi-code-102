from copy import copy
from cryptography.fernet import Fernet
import hashlib
import random


def self_consistency_check() -> bool:
    random.seed(0)
    a = list(range(50))
    random.shuffle(a)
    if a == [
        43,
        1,
        28,
        14,
        36,
        12,
        0,
        27,
        47,
        7,
        33,
        34,
        20,
        49,
        5,
        38,
        11,
        23,
        40,
        15,
        10,
        21,
        46,
        3,
        9,
        4,
        41,
        42,
        39,
        17,
        29,
        45,
        6,
        35,
        18,
        8,
        44,
        13,
        37,
        22,
        30,
        19,
        25,
        31,
        32,
        16,
        2,
        26,
        48,
        24,
    ]:
        return True
    else:
        return False


def check_hashseed() -> bool:
    """Need to set PYTHONHASHSEED=0 in env variable"""
    if hash("GOD") == -3890164749404887474:
        print("Hash seed confirmed.")
        return True
    else:
        print("Hash seed incorrect.")
        return False


def permutate(input: str, key: str = None):
    """Input should be a space delimited word string"""
    if not self_consistency_check():
        print("Failed self consistency check. DO NOT PROCEED!")
        quit(1)

    if not key:
        print("No key specified, will used the default: test")
        key = "test"

    words = [w.strip() for w in input.split()]
    wc = len(words)
    seq_orig = list(range(wc))
    seq = copy(seq_orig)
    m = hashlib.sha256()
    m.update(key.encode() if isinstance(key, str) else key)
    random.seed(m.hexdigest())
    random.shuffle(seq)
    return " ".join([words[i] for i in seq])


def reverse_permutate(input: str, key: str = None):
    """Input should be a space delimited word string"""
    if not self_consistency_check():
        print("Failed self consistency check. DO NOT PROCEED!")
        quit(1)

    if not key:
        print("No key specified, will used the default: test")
        key = "test"

    words = [w.strip() for w in input.split()]
    wc = len(words)
    seq_orig = list(range(wc))
    seq = copy(seq_orig)
    m = hashlib.sha256()
    m.update(key.encode() if isinstance(key, str) else key)
    random.seed(m.hexdigest())
    random.shuffle(seq)
    tp = list(zip(seq_orig, seq))
    tp.sort(key=lambda x: x[1])
    seq_rev = [t[0] for t in tp]
    return " ".join([words[i] for i in seq_rev])


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)
