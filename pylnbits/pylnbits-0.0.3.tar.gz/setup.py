# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylnbits']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.4.1', 'aiohttp==3.7.4.post0', 'pre-commit==2.13.0']

setup_kwargs = {
    'name': 'pylnbits',
    'version': '0.0.3',
    'description': 'Python library for LNBits.',
    'long_description': None,
    'author': 'bitkarrot',
    'author_email': 'bitkarrot@bitcoin.org.hk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
