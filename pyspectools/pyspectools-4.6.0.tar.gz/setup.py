# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyspectools',
 'pyspectools.astro',
 'pyspectools.mmw',
 'pyspectools.models',
 'pyspectools.qchem',
 'pyspectools.spectra']

package_data = \
{'': ['*'], 'pyspectools': ['mpl_stylesheets/*', 'templates/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'PeakUtils>=1.3.2',
 'astropy==4.3.1',
 'astroquery==0.4.3',
 'bokeh>=2.4.0,<3.0.0',
 'colorlover>=0.3.0,<0.4.0',
 'ipython>=7.28.0,<8.0.0',
 'ipywidgets>=7.6.5,<8.0.0',
 'joblib>=1.0.1,<2.0.0',
 'lmfit>=1.0.2,<2.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'monsterurl>=0.2,<0.3',
 'networkx>=2.6.3,<3.0.0',
 'numba>=0.54.0,<0.55.0',
 'numpy>=1.16',
 'pandas>=1.3.3,<2.0.0',
 'paramiko>=2.7.2,<3.0.0',
 'periodictable>=1.6.0,<2.0.0',
 'plotly>=3.0.0',
 'ruamel.yaml>=0.17.16,<0.18.0',
 'scipy>=1.7.1,<2.0.0',
 'sklearn>=0.0,<0.1',
 'tinydb>=4.5.2,<5.0.0',
 'torch>=1.9.1,<2.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'uncertainties>=3.1.6,<4.0.0']

setup_kwargs = {
    'name': 'pyspectools',
    'version': '4.6.0',
    'description': 'A set of Python tools/routines for spectroscopy',
    'long_description': None,
    'author': 'Kelvin Lee',
    'author_email': 'kin.long.kelvin.lee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laserkelvin/PySpecTools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10.0',
}


setup(**setup_kwargs)
