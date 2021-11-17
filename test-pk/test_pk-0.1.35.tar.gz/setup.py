# coding: utf-8

import os
import re
from functools import reduce

from setuptools import find_packages
from setuptools import setup

pwd = os.path.dirname(__file__)

extra_reqs = {
  'collector_api': [
    'openpyxl>=3.0.8',
    'decorator==4.4.2',
  ],
}
extra_reqs['all'] = sorted(set(reduce(lambda x, y: x + y, extra_reqs.values())))

with open(os.path.join(pwd, 'lib', 'test_pk', '__init__.py')) as f:
  VERSION = (
    re.compile(r""".*__version__ = ["'](.*?)['"]""", re.S)
      .match(f.read())
      .group(1)
  )

setup(name='test_pk',
      version=VERSION,
      long_description='',
      long_description_content_type='text/markdown',
      packages=find_packages('lib'),
      include_package_data=True,
      package_dir={
        '': 'lib',
      },
      platforms='any',
      install_requires=[
        'sqlalchemy>=1.3.0',
        'jsonschema>=3.2.0',
      ],
      extras_require=extra_reqs,
      python_requires='>=3',
      keywords='sqlalchemy',
      )
