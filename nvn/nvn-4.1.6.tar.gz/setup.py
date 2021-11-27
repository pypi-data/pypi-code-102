# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nvn']

package_data = \
{'': ['*']}

install_requires = \
['ardlib', 'click', 'pyyaml', 'watchgod']

entry_points = \
{'console_scripts': ['nvn = nvn.__main__:main']}

setup_kwargs = {
    'name': 'nvn',
    'version': '4.1.6',
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
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
