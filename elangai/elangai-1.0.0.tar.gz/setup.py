# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


import os
import subprocess

from os.path import abspath, dirname, join
from setuptools import setup
from setuptools import find_packages


# The directory containing this file
HERE = abspath(dirname(__file__))


# The text of the README file
with open(join(HERE, "README.md")) as fid:
    README = fid.read()


with open(os.path.join("elangai", "version.txt")) as f:
    version = f.read().strip()


setup(name='elangai',
      version=version,
      description='Inference Engine Platform on Edge Device.',
      long_description=README,
      long_description_content_type="text/markdown",
      author='elangai Developer',
      author_email='resha.alfahsi@techbros.io',
      url='https://www.elang.ai/',
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: Other/Proprietary License",
          "Topic :: Scientific/Engineering :: Artificial Intelligence",
          "Topic :: Software Development :: Libraries :: Application Frameworks",
          "Programming Language :: Python :: 3.6",
      ],
      include_package_data=True,
      install_requires=[
          'typer',
      ],
      package_data={
            'elangai': [
                'version.txt',
                'template/app_name/config.json-tpl',
                'template/app_name/main.py-tpl',
                'template/app_name/utils/*.py-tpl',
            ],
      },
      packages=find_packages(),
      entry_points={"console_scripts": ["elangai=elangai.__main__:app"]},
      )
