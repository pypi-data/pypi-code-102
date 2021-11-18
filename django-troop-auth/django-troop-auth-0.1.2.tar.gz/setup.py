# !/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="django-troop-auth",
    version="0.1.2",
    url="https://github.com/troopstack/django-troop-auth.git",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["django<=3.2.10", "djangorestframework", "djangorestframework-jwt", "django-json-rpc"]
)