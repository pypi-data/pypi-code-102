from copy import copy
from cryptography.fernet import Fernet
import fire
import hashlib
import random


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
