# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['launcha']

package_data = \
{'': ['*'], 'launcha': ['template/*', 'template/modules/cleanrl/*']}

install_requires = \
['boto3>=1.20.7,<2.0.0', 'requests>=2.26.0,<3.0.0', 'wandb>=0.12.6,<0.13.0']

entry_points = \
{'console_scripts': ['launcha = launcha.launcha:main']}

setup_kwargs = {
    'name': 'launcha',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Costa Huang',
    'author_email': 'costa.huang@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
