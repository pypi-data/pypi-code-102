# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datto', 'datto.data']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.3.0,<5.0.0',
 'catboost>=1.0.3,<2.0.0',
 'gensim>=4.1.2,<5.0.0',
 'hypothesis>=6.24.5,<7.0.0',
 'lightgbm>=3.3.1,<4.0.0',
 'lime>=0.2.0,<0.3.0',
 'nltk>=3.6.5,<4.0.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'progressbar>=2.5,<3.0',
 'psycopg2-binary>=2.9.2,<3.0.0',
 'python-json-logger>=2.0.2,<3.0.0',
 's3fs>=2021.11.0,<2022.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'shap>=0.40.0,<0.41.0',
 'sklearn>=0.0,<0.1',
 'spacy>=3.2.0,<4.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0',
 'statsmodels>=0.13.1,<0.14.0',
 'tabulate>=0.8.9,<0.9.0',
 'wheel>=0.37.0,<0.38.0',
 'xgboost>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'datto',
    'version': '0.7.2',
    'description': 'Data Tools (Dat To)',
    'long_description': None,
    'author': 'kristiewirth',
    'author_email': 'kristie.ann.wirth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
