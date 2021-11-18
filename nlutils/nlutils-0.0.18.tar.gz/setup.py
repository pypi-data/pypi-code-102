from setuptools import find_packages, setup

from distutils.core import setup

setup(name = "nlutils",
    version = "0.0.18",
    description = "Toolkit for neural learning training",
    author = "Nikola Liu",
    author_email = "nikolaliu@icloud.com",
    py_modules=['nlutils'],
    packages = find_packages(),
    install_requires=[
        'coloredlogs',
        'tqdm',
        'itchat',
        'smtplib',
        'email'
    ],
)