#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension


factorial_module = Extension('_factorial-factor',
                           sources=['factor_wrap.cxx', 'factor.cpp'],
                           )

setup (name = 'examplefactor',
       version = '0.3',
       author      = "Pradeesh",
       description = """Simple factorial calculators""",
       ext_modules = [factorial_module],
       py_modules = ["example"],
       )
