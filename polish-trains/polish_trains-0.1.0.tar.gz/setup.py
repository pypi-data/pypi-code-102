# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polish_trains']

package_data = \
{'': ['*']}

install_requires = \
['async_generator==1.10',
 'attrs==21.2.0',
 'beautifulsoup4==4.10.0',
 'certifi==2021.10.8',
 'cffi==1.15.0',
 'cryptography==35.0.0',
 'h11==0.12.0',
 'idna==3.3',
 'outcome==1.1.0',
 'pyOpenSSL==21.0.0',
 'pycparser==2.21',
 'selenium==4.0.0',
 'six==1.16.0',
 'sniffio==1.2.0',
 'sortedcontainers==2.4.0',
 'soupsieve==2.3.1',
 'trio-websocket==0.9.2',
 'trio==0.19.0',
 'urllib3==1.26.7',
 'wsproto==1.0.0']

setup_kwargs = {
    'name': 'polish-trains',
    'version': '0.1.0',
    'description': 'Search polish trains via simple API.',
    'long_description': None,
    'author': 'Konrad Nowara',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
