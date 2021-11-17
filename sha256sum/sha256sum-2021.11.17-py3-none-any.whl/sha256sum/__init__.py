"""Compute SHA256 message digest from a file"""

from hashlib import sha256

BLOCK_SIZE = 128 * 1024


def sha256sum(filename: str) -> str:
    """Compute SHA256 message digest from a file"""
    hash_func = sha256()
    byte_array = bytearray(BLOCK_SIZE)
    memory_view = memoryview(byte_array)
    with open(filename, "rb", buffering=0) as file:
        for block in iter(lambda: file.readinto(memory_view), 0):
            hash_func.update(memory_view[:block])
    return hash_func.hexdigest()
