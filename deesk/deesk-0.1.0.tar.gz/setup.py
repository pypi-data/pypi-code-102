# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deesk', 'deesk.drivers']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.7.0,<0.8.0', 'anyio>=3.3.1,<4.0.0', 'yarl>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'deesk',
    'version': '0.1.0',
    'description': 'Async storages for Python.',
    'long_description': '# Deesk\n\nAsync storages for Python.\n\n![PyPI](https://img.shields.io/pypi/v/deesk)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/alex-oleshkevich/deesk/Lint)\n![GitHub](https://img.shields.io/github/license/alex-oleshkevich/deesk)\n![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/deesk)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/deesk)\n![GitHub Release Date](https://img.shields.io/github/release-date/alex-oleshkevich/deesk)\n![Lines of code](https://img.shields.io/tokei/lines/github/alex-oleshkevich/deesk)\n\n## Installation\n\nInstall `deesk` using PIP or poetry:\n\n```bash\npip install deesk\n# or\npoetry add deesk\n```\n\n## Features\n\n-   TODO\n\n## Quick start\n\nSee example application in `examples/` directory of this repository.\n',
    'author': 'Alex Oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alex-oleshkevich/deesk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
