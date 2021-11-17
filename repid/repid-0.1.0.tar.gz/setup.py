# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['repid']

package_data = \
{'': ['*']}

install_requires = \
['aioredis[hiredis]>=2.0.0,<3.0.0', 'orjson>=3.6.4,<4.0.0']

setup_kwargs = {
    'name': 'repid',
    'version': '0.1.0',
    'description': 'Async Redis queue for Python.',
    'long_description': None,
    'author': 'aleksul',
    'author_email': 'aleksandrsulimov@bk.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
