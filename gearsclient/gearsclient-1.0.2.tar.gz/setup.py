# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gearsclient']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=1.6.0,<2.0.0', 'redis==3.5.3', 'six>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'gearsclient',
    'version': '1.0.2',
    'description': 'RedisGears Python Client',
    'long_description': "[![license](https://img.shields.io/github/license/RedisGears/redisgears-py.svg)](https://github.com/RedisGears/redisgears-py)\n[![PyPI version](https://badge.fury.io/py/redisgears-py.svg)](https://badge.fury.io/py/redisgears-py)\n[![CircleCI](https://circleci.com/gh/RedisGears/redisgears-py/tree/master.svg?style=svg)](https://circleci.com/gh/RedisGears/redisgears-py/tree/master)\n[![GitHub issues](https://img.shields.io/github/release/RedisGears/redisgears-py.svg)](https://github.com/RedisGears/redisgears-py/releases/latest)\n[![Codecov](https://codecov.io/gh/RedisGears/redisgears-py/branch/master/graph/badge.svg)](https://codecov.io/gh/RedisGears/redisgears-py)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/RedisGears/redisgears-py.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/RedisGears/redisgears-py/context:python)\n[![Known Vulnerabilities](https://snyk.io/test/github/RedisJSON/redisjson-py/badge.svg?targetFile=pyproject.toml)](https://snyk.io/test/github/RedisJSON/redisjson-py?targetFile=pyproject.toml)\n\n# redisgears-py\n[![Forum](https://img.shields.io/badge/Forum-RedisGears-blue)](https://forum.redislabs.com/c/modules/redisgears)\n[![Discord](https://img.shields.io/discord/697882427875393627?style=flat-square)](https://discord.gg/6yaVTtp)\n\n[RedisGears](http://redisgears.io) python client (support python3 only!)\n\n## Example: Using the Python Client:\n```python\nfrom gearsclient import GearsRemoteBuilder as GearsBuilder\nfrom gearsclient import execute\nimport redis\n\nconn = redis.Redis(host='localhost', port=6379)\n\n# count for each genre how many times it appears\n\nres = GearsBuilder('KeysOnlyReader', r=conn).\\\n\t  map(lambda x:execute('hget', x, 'genres')).\\\n\t  filter(lambda x:x != '\\\\N').\\\n\t  flatmap(lambda x: x.split(',')).\\\n\t  map(lambda x: x.strip()).\\\n\t  countby().\\\n\t  run()\n\n\nfor r in res[0]:\n\tprint('%-15s: %d' % (r['key'], r['value']))\n```\n\n## Installing\n```\npip install git+https://github.com/RedisGears/redisgears-py.git\n```\nNotice that the library also need to be installed in RedisGears virtual env.\n\n## Developing\n\n1. Create a virtualenv to manage your python dependencies, and ensure it's active.\n   ```virtualenv -v venv```\n2. Install [pypoetry](https://python-poetry.org/) to manage your dependencies.\n   ```pip install poetry```\n3. Install dependencies.\n   ```poetry install```\n\n[tox](https://tox.readthedocs.io/en/latest/) runs all tests as its default target. Running *tox* by itself will run unit tests. Ensure you have a running redis, with the module loaded.\n\n\n",
    'author': 'RedisLabs',
    'author_email': 'oss@redislabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
