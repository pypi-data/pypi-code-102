# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ned', 'ned.candidate_generation', 'ned.metrics']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ned',
    'version': '1.0.0',
    'description': 'entity linking, named-entity disambiguation, record linkage',
    'long_description': None,
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
