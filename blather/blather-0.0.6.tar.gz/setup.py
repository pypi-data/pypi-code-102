#!/usr/bin/env python

from setuptools import setup

setup(
    name='blather',
    version='0.0.6',
    packages=['blather'],
    install_requires=[
        'torch',
        'transformers',
    ],
)
