# !/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="django-troop-auth",
    version="0.1.0",
    url="https://github.com/troopstack/django-troop-auth.git",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["django", "djangorestframework", "djangorestframework-jwt", "django-json-rpc"]
)