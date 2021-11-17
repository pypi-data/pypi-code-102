# Copyright (C) 2021 Matthias Nadig

from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='logbox',
    version='1.0.0',
    description='Toolbox for terminal output and logging to file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matthias Nadig',
    author_email='matthias.nadig@yahoo.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
)
