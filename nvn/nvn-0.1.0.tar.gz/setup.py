# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nvn']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nvn',
    'version': '0.1.0',
    'description': 'nvn',
    'long_description': None,
    'author': 'Ardustri',
    'author_email': 'social.linter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
