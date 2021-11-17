# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astrochem_ml', 'astrochem_ml.smiles', 'astrochem_ml.smiles.tests']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0',
 'periodictable>=1.6.0,<2.0.0',
 'rdkit-pypi>=2021.9.2,<2022.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'selfies>=2.0.0,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'astrochem-ml',
    'version': '0.1.0',
    'description': 'Cheminformatics tools for astrochemistry',
    'long_description': None,
    'author': 'Kelvin Lee',
    'author_email': 'kin.long.kelvin.lee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
