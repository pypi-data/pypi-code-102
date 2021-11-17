#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

try:
    from setuptools import setup, Extension, sysconfig
    setup
except ImportError:
    from distutils.core import setup, Extension
    from distutils import sysconfig
    setup

with open("README.md", "r") as fh:
    long_description = fh.read()

import re
VERSIONFILE="baccoemu/_version.py"
if not os.path.isfile(VERSIONFILE):
    verstr = '1.1.2'
    f = open(VERSIONFILE,"w")
    f.write("__version__ = \"{}\"".format(verstr))
    f.close()
else:
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name="baccoemu",
    author="Raul E Angulo",
    author_email="rangulo@dipc.org",
    version=verstr,
    description="Matter power spectrum emulator",
    url="http://dipc.org/bacco/",
    license="MIT",
    packages=['baccoemu'],
    package_data={
        "baccoemu": ["LICENSE", "AUTHORS.rst"],
        "": ["*.pkl"]
    },
    include_package_data=True,
    install_requires=["numpy", "sklearn", "keras",  "matplotlib", "scipy",
                      "tensorflow", "setuptools", "requests", "progressbar2"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    python_requires='>=3.6',
)
