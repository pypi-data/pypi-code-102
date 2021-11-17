import sys
from setuptools import setup

message = "You've been owned. Ask @shantanu for more details."

if "install" in sys.argv or "bdist_wheel" in sys.argv:
    raise Exception(message)

setup(
    name="rcall",
    version="0.1.0",
    long_description=message,
)
