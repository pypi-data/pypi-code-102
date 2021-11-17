# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ndradexhyperfine']

package_data = \
{'': ['*'],
 'ndradexhyperfine': ['bin/.git',
                      'bin/.git',
                      'bin/.git',
                      'bin/.git',
                      'bin/.git',
                      'bin/.git',
                      'bin/.gitignore',
                      'bin/.gitignore',
                      'bin/.gitignore',
                      'bin/.gitignore',
                      'bin/.gitignore',
                      'bin/.gitignore',
                      'bin/.travis.yml',
                      'bin/.travis.yml',
                      'bin/.travis.yml',
                      'bin/.travis.yml',
                      'bin/.travis.yml',
                      'bin/.travis.yml',
                      'bin/LICENSE',
                      'bin/LICENSE',
                      'bin/LICENSE',
                      'bin/LICENSE',
                      'bin/LICENSE',
                      'bin/LICENSE',
                      'bin/Makefile',
                      'bin/Makefile',
                      'bin/Makefile',
                      'bin/Makefile',
                      'bin/Makefile',
                      'bin/Makefile',
                      'bin/README.md',
                      'bin/README.md',
                      'bin/README.md',
                      'bin/README.md',
                      'bin/README.md',
                      'bin/README.md']}

install_requires = \
['astropy>=4.0,<5.0',
 'astroquery>=0.4,<0.5',
 'netcdf4>=1.5,<2.0',
 'numpy>=1.18,<2.0',
 'pandas>=0.25,<1.2',
 'toml>=0.10,<0.11',
 'tqdm>=4.41,<5.0',
 'xarray>=0.15,<0.16']

setup_kwargs = {
    'name': 'ndradexhyperfine',
    'version': '0.2.4',
    'description': 'Python package for RADEX grid calculation',
    'long_description': None,
    'author': 'Thomas Williams',
    'author_email': 'williams@mpia.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
