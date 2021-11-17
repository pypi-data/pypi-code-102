#!/usr/bin/env python

"""
    Bookizer
    ==========

    Bookizer get's an almost uncertain number of CSV files and converts them into a big CSV/ODS/XLS/XLSX file

"""

import sys

from setuptools import setup

if sys.version_info.major < 3:
    raise RuntimeError(
        'Bookizer does not support Python 2.x anymore. '
        'Please use Python 3 or do magic.')

setup()
