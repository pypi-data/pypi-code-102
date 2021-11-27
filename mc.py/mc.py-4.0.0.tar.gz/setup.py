# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mc', 'mc.builtin']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mc.py',
    'version': '4.0.0',
    'description': 'Python package which provides you a simple way to generate phrases using Markov chains',
    'long_description': '# mc.py\n**mc.py** is a tiny and trivial Python package which provides you \na simple way to generate phrases using Markov chains.\n\nDocs can be found [here](https://jieggii.github.io/mc.py).\n\n## Installation\nJust install it using **pip** or any other package manager you use... \nShould I seriously teach you this?\n\n`pip install mc.py`\n\n## Simple usage example\n_More examples can be found [here](https://github.com/jieggii/mc.py/tree/master/examples)._\n\n```python\nimport mc\nfrom mc.builtin import validators\n\n\ngenerator = mc.PhraseGenerator(\n    samples=["hello world", "world of cuties", "bruh"]\n)\nphrase = generator.generate_phrase(\n    validators=[validators.words_count(minimal=4)]\n)\n\nprint(phrase)\n# >>> "hello world of cuties"\n```\n\n## Links\n* [Documentation](https://jieggii.github.io/mc.py)\n* [Examples](https://github.com/jieggii/mc.py/tree/master/examples)\n* [Package at PyPi](https://pypi.org/project/mc.py)',
    'author': 'jieggii',
    'author_email': 'jieggii.contact@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jieggii/mc.py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
