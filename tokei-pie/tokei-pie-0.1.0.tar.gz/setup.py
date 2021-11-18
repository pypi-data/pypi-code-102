# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tokei_pie']

package_data = \
{'': ['*']}

install_requires = \
['plotly>=5.4.0,<6.0.0']

entry_points = \
{'console_scripts': ['tokei-pie = tokei_pie.main:main']}

setup_kwargs = {
    'name': 'tokei-pie',
    'version': '0.1.0',
    'description': 'Draw a pie chart for tokei output.',
    'long_description': None,
    'author': 'laixintao',
    'author_email': 'laixintaoo@gmail.com',
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
