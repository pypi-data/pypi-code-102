# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cipher_asa2249']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.5,<7.0.0']

setup_kwargs = {
    'name': 'cipher-asa2249',
    'version': '0.1.0',
    'description': 'A package for eencrypting and decrypting text using the cipher algorithm.',
    'long_description': "# cipher_asa2249\n\nA package for running Julius Caesar's cipher algorithm to encrypt and decrpyt text. This algorithm takes in \nan integer, shift, and a body of text, text, as well as a boolean for encrypt as\nimplicit parameters.\n\nThe integers shift determines the amount that each character is shifted in text.\n\nFor example, if shift = 3, and the word is 'cat', each letter will be shifted 3\nto the right. Hence, 'cat' becomes 'fdw'.\n\n## Installation\n\n```bash\n$ pip install cipher_asa2249\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`cipher_asa2249` was created by Armaan Ahmed. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`cipher_asa2249` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Armaan Ahmed',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
