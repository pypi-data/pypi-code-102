# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nvn']

package_data = \
{'': ['*']}

install_requires = \
['click', 'pyyaml', 'watchgod']

setup_kwargs = {
    'name': 'nvn',
    'version': '4.1.0',
    'description': 'nvn',
    'long_description': None,
    'author': 'Ardustri',
    'author_email': 'social.linter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
