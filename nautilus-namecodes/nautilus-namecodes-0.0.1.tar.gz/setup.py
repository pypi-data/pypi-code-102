# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nautilus_namecodes',
 'nautilus_namecodes.builder',
 'nautilus_namecodes.format',
 'nautilus_namecodes.scheme.v_0_0_1']

package_data = \
{'': ['*']}

install_requires = \
['atoml>=1.1.0,<2.0.0', 'tox>=3.24.4,<4.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['nautilus-namecodes = nautilus_namecodes.main:app']}

setup_kwargs = {
    'name': 'nautilus-namecodes',
    'version': '0.0.1',
    'description': 'Nautilus Filename Specification (nautilus-namecodes)',
    'long_description': '# Nautilus Filename Specification\n\n## [💠 View Project Documentation 📖](https://nautilus-namecodes.readthedocs.io/en/latest/)\n\n### (nautilus-namecodes)\n\n*Nautilus namecodes are encoded filenames for media and other artistic creations in filesystem based content management systems.*\n\n### Command Line Interface:\n\nThis application can be launched from the command line.\n\n### Libraries Used\n\n* This project depends on \'atoml\' for processing the pyproject.toml file.\n  \n  MIT License Copyright (c) 2021 Frost Ming, 2018 Sébastien Eustace\n\n  > [https://github.com/frostming/atoml](https://github.com/frostming/atoml)\n\n* This project depends on \'typer\' for creating the CLI.\n\n  MIT License Copyright (c) 2019 Sebastián Ramírez\n\n  > [https://github.com/tiangolo/typer](https://github.com/tiangolo/typer)\n\n### Notes\n\n* This repository uses "pytest" to run python tests code.\n\n> [https://docs.pytest.org/en/latest/](https://docs.pytest.org/en/latest/)\n\n* This repository uses "Black" to format python code.\n\n> [https://black.readthedocs.io/en/latest/](https://black.readthedocs.io/en/latest/)\n\n* This repository uses "mypy" to type check the python code.\n\n> [https://github.com/python/mypy](https://github.com/python/mypy)\n\n* This repository uses \'pylint\' to check the python code quality.\n\n> [https://pylint.org/](https://pylint.org/)\n\n* This repository uses \'bandit\' to code for security issues.\n\n> [https://bandit.readthedocs.io/en/latest/](https://bandit.readthedocs.io/en/latest/)\n\n* This repository uses \'isort\' to check that imports are sorted.\n\n> [https://pycqa.github.io/isort/](https://pycqa.github.io/isort/)\n\n* This repository uses Sphinx and Myst-Parser for documentation infrastructure.\n\n> [https://www.sphinx-doc.org/en/master/](https://www.sphinx-doc.org/en/master/)\n> [https://github.com/executablebooks/MyST-Parser](https://github.com/executablebooks/MyST-Parser)\n\n\n### Instructions\n\nThis repository uses [Poetry: Dependency Management for Python].\n\n1. Install Python.\n\n> [https://www.python.org/downloads/](https://www.python.org/downloads/)\n\n2. Install Poetry.\n\n> [https://github.com/python-poetry/poetry](https://github.com/python-poetry/poetry)\n\n3. Clone the `nautilus-filename_specification` repository.\n\n> [https://github.com/da2ce7/nautilus-filename_specification/tree/develop](https://github.com/da2ce7/nautilus-filename_specification/tree/develop)\n\n4. Change Directory to the cloned repository:\n\n> `cd nautilus-filename_specification`\n\n5. Install Dependencies:\n\n> `poetry install`\n\n6. Run Tests:\n\n> `poetry run tox`\n\n7. Create Distribution Package:\n\n> `poetry build`\n\n[poetry: dependency management for python]: https://python-poetry.org/\n',
    'author': 'Cameron Garnham',
    'author_email': 'cameron@nautilus-cyberneering.de',
    'maintainer': 'Cameron Garnham',
    'maintainer_email': 'cameron@nautilus-cyberneering.de',
    'url': 'https://github.com/da2ce7/nautilus-filename_specification',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
