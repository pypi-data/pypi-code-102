#!/usr/bin/env python3

import os
from setuptools import setup, find_packages
PKG_NAME="flavuer"

def package_files(directory):
    paths = []
    for root, _, files in os.walk(directory):
        root_strip = root.lstrip(f'{PKG_NAME}/')
        for filename in files:
            paths.append(os.path.join(root_strip, filename))
    return paths

setup(
    name=PKG_NAME,
    version='0.0.dev.1',
    description='Flask + VueJS',
    url='https://github.com/flavuer/flavuer',
    author='darless',
    author_email='darless1000@gmail.com',
    packages=find_packages(exclude=('tests')),
    python_requires='>=3.8',
    install_requires=[
        'colorama'
    ],
    # Package data
    package_data = {
        '': package_files('flavuer/template/app'),
    },
    entry_points={
        'console_scripts': [
            'flavuer = flavuer.__main__:main'
        ]
    },
)
