# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['astrochem_embedding',
 'astrochem_embedding.layers',
 'astrochem_embedding.layers.tests',
 'astrochem_embedding.models',
 'astrochem_embedding.models.tests',
 'astrochem_embedding.pipeline',
 'astrochem_embedding.pipeline.tests']

package_data = \
{'': ['*'], 'astrochem_embedding.models': ['pretrained/*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'ipython>=7.28.0,<8.0.0',
 'palettable>=3.3.0,<4.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pytorch-lightning>=1.4.8,<2.0.0',
 'rdkit-pypi>=2021.9.2,<2022.0.0',
 'ruamel.yaml>=0.17.17,<0.18.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'selfies>=2.0.0,<3.0.0',
 'torch>=1.10.0,<2.0.0',
 'torchinfo>=1.5.3,<2.0.0',
 'torchvision>=0.11.0,<0.12.0',
 'wandb>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'astrochem-embedding',
    'version': '0.1.2',
    'description': 'Language models for astrochemistry',
    'long_description': "Language models for astrochemistry\n==================================\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/astrochem_embedding.svg\n   :target: https://pypi.org/project/astrochem_embedding/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/astrochem_embedding.svg\n   :target: https://pypi.org/project/astrochem_embedding/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/astrochem_embedding\n   :target: https://pypi.org/project/astrochem_embedding\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/astrochem_embedding\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/astrochem_embedding/latest.svg?label=Read%20the%20Docs\n   :target: https://astrochem_embedding.readthedocs.io/\n   :alt: Read the documentation at https://astrochem_embedding.readthedocs.io/\n.. |Tests| image:: https://github.com/laserkelvin/astrochem_embedding/workflows/Tests/badge.svg\n   :target: https://github.com/laserkelvin/astrochem_embedding/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/laserkelvin/astrochem_embedding/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/laserkelvin/astrochem_embedding\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nThe project environment for Language models for astrochemistry is controlled by `conda` \nand `poetry`; the former for maintaining the Python environment, as well as additional \nlibraries like CUDA, and the latter for Python specific dependencies. There is\na bit of overlap between these two tools, however mostly because `conda`\nis not great for resolving dependencies, and `poetry` can't handle things\nthat aren't Python (e.g. MPI, MKL).\n\nThe recommended procedure from scratch is to follow these steps:\n\n.. code:: console\n\n   $ conda create -n astrochem_embedding python=3.7\n   $ conda activate astrochem_embedding\n   $ pip install poetry\n   $ poetry install\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nProject Structure\n-----------------\n\nThe project filestructure is laid out as such::\n\n   ├── CITATION.cff\n   ├── codecov.yml\n   ├── CODE_OF_CONDUCT.rst\n   ├── CONTRIBUTING.rst\n   ├── data\n   │\xa0\xa0 ├── external\n   │\xa0\xa0 ├── interim\n   │\xa0\xa0 ├── processed\n   │\xa0\xa0 └── raw\n   ├── docs\n   │\xa0\xa0 ├── codeofconduct.rst\n   │\xa0\xa0 ├── conf.py\n   │\xa0\xa0 ├── contributing.rst\n   │\xa0\xa0 ├── index.rst\n   │\xa0\xa0 ├── license.rst\n   │\xa0\xa0 ├── reference.rst\n   │\xa0\xa0 ├── requirements.txt\n   │\xa0\xa0 └── usage.rst\n   ├── environment.yml\n   ├── models\n   ├── notebooks\n   │\xa0\xa0 ├── dev\n   │\xa0\xa0 ├── exploratory\n   │\xa0\xa0 └── reports\n   ├── noxfile.py\n   ├── poetry.lock\n   ├── pyproject.toml\n   ├── README.rst\n   ├── scripts\n   │\xa0\xa0 └── train.py\n   └── src\n      └── astrochem_embedding\n         ├── __init__.py\n         ├── layers\n         │\xa0\xa0 ├── __init__.py\n         │\xa0\xa0 ├── layers.py\n         │\xa0\xa0 └── tests\n         │\xa0\xa0     ├── __init__.py\n         │\xa0\xa0     └── test_layers.py\n         ├── __main__.py\n         ├── models\n         │\xa0\xa0 ├── __init__.py\n         │\xa0\xa0 ├── models.py\n         │\xa0\xa0 └── tests\n         │\xa0\xa0     ├── __init__.py\n         │\xa0\xa0     └── test_models.py\n         ├── pipeline\n         │\xa0\xa0 ├── data.py\n         │\xa0\xa0 ├── __init__.py\n         │\xa0\xa0 ├── tests\n         │\xa0\xa0 │\xa0\xa0 ├── __init__.py\n         │\xa0\xa0 │\xa0\xa0 ├── test_data.py\n         │\xa0\xa0 │\xa0\xa0 └── test_transforms.py\n         │\xa0\xa0 └── transforms.py\n         └── utils.py\n\nA brief summary of what each folder is designed for:\n\n#. `data` contains copies of the data used for this project. It is recommended to form a pipeline whereby the `raw` data is preprocessed, serialized to `interim`, and when ready for analysis, placed into `processed`.\n#. `models` contains serialized weights intended for distribution, and/or testing.\n#. `notebooks` contains three subfolders: `dev` is for notebook based development, `exploratory` for data exploration, and `reports` for making figures and visualizations for writeup.\n#. `scripts` contains files that meant for headless routines, generally those with long compute times such as model training and data cleaning.\n#. `src/astrochem_embedding` contains the common code base for this project.\n\n\nCode development\n----------------\n\nAll of the code used for this project should be contained in `src/astrochem_embedding`,\nat least in terms of the high-level functionality (i.e. not scripts), and is intended to be\na standalone Python package.\n\nThe package is structured to match the abstractions for deep learning, specifically PyTorch, \nPyTorch Lightning, and Weights and Biases, by separating parts of data structures and processing\nand model/layer development.\n\nSome concise tenets for development\n\n* Write unit tests as you go.\n* Commit changes, and commit frequently. Write `semantic`_ git commits!\n* Formatting is done with ``black``; don't fuss about it 😃\n* For new Python dependencies, use `poetry add <package>`.\n* For new environment dependencies, use `conda env export -f environment.yml`.\n\nNotes on best practices, particularly regarding CI/CD, can be found in the extensive\ndocumentation for the `Hypermodern Python Cookiecutter`_ repository.\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Language models for astrochemistry* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@laserkelvin`_'s PyTorch Project Cookiecutter, \na fork of  `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/laserkelvin/astrochem_embedding/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://astrochem_embedding.readthedocs.io/en/latest/usage.html\n.. _semantic: https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716\n.. _@laserkelvin: https://github.com/laserkelvin\n",
    'author': 'Kelvin Lee',
    'author_email': 'kin.long.kelvin.lee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laserkelvin/astrochem_embedding',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
