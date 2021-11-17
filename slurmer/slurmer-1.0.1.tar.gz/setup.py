# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurmer']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'slurmer',
    'version': '1.0.1',
    'description': 'A package to schedule different tasks in parallel with cluster support.',
    'long_description': '# Slurmer\n\nThis package is designed to run heavy loads in a computer cluster. \n\nFor now we only support the SLURM task scheduler but PRs are welcome.\n\nYou can find the documentation [here](https://jmigual.github.io/slurmer/)\n',
    'author': 'Joan Marcè i Igual',
    'author_email': 'J.Marce.i.Igual@tue.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jmigual.github.io/slurmer/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
