# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['obplatform']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{'pandas': ['pandas>=1.3.4,<2.0.0']}

setup_kwargs = {
    'name': 'obplatform',
    'version': '0.1.0',
    'description': 'APIs to access ASHRAE OB Database',
    'long_description': None,
    'author': 'Wei Mu',
    'author_email': 'wmu100@syr.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
