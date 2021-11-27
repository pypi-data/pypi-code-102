# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchminer', 'torchminer.plugins']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.31.0,<3.0.0',
 'ipython>=7.29.0,<8.0.0',
 'matplotlib>=3.5.0,<4.0.0',
 'tensorboardX>=2.4.1,<3.0.0',
 'torch>=1.10.0,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'torchminer',
    'version': '0.2.1',
    'description': 'Run Torch With A Simple Miner',
    'long_description': 'This Project is Forked From [MineTorch](https://github.com/louis-she/minetorch).\n\nPublished on [pypi](https://pypi.org/project/torchminer/)\n\nPackaged Using [Poetry](https://python-poetry.org/)',
    'author': 'InEase',
    'author_email': 'inease28@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
