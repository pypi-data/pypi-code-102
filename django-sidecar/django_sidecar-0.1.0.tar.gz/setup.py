#!/usr/bin/env python

from distutils.core import setup
from django_sidecar import __version__

setup(name='django_sidecar',
      version=__version__,
      description='django sidecar pattern implementation',
      author='svtter',
      author_email='svtter@163.com',
      url='',
      packages=['django_sidecar'],
     )