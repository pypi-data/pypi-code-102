#!/usr/bin/python
# encoding: utf-8

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="asgidphoto",
    version="0.0.1",
    license="MIT Licence",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["requests>=2.19.1"]
)
