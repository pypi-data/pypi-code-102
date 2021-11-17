# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redisbloom']

package_data = \
{'': ['*']}

install_requires = \
['hiredis>=2.0.0,<3.0.0',
 'redis==3.5.3',
 'rmtest>=0.7.0,<0.8.0',
 'six>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'redisbloom-py',
    'version': '0.4.1',
    'description': 'RedisBloom Python Client',
    'long_description': "[![license](https://img.shields.io/github/license/RedisBloom/redisbloom-py.svg)](https://github.com/RedisBloom/redisbloom-py)\n[![PyPI version](https://badge.fury.io/py/redisbloom.svg)](https://badge.fury.io/py/redisbloom)\n[![CircleCI](https://circleci.com/gh/RedisBloom/redisbloom-py/tree/master.svg?style=svg)](https://circleci.com/gh/RedisBloom/redisbloom-py/tree/master)\n[![GitHub issues](https://img.shields.io/github/release/RedisBloom/redisbloom-py.svg)](https://github.com/RedisBloom/redisbloom-py/releases/latest)\n[![Codecov](https://codecov.io/gh/RedisBloom/redisbloom-py/branch/master/graph/badge.svg)](https://codecov.io/gh/RedisBloom/redisbloom-py)\n[![Known Vulnerabilities](https://snyk.io/test/github/RedisBloom/redisbloom-py/badge.svg?targetFile=pyproject.toml)](https://snyk.io/test/github/RedisBloom/redisbloom-py?targetFile=pyproject.toml)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/RedisBloom/redisbloom-py.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/RedisBloom/redisbloom-py/alerts/)\n\n# Python client for RedisBloom\n[![Forum](https://img.shields.io/badge/Forum-RedisBloom-blue)](https://forum.redis.com/c/modules/redisbloom)\n[![Discord](https://img.shields.io/discord/697882427875393627?style=flat-square)](https://discord.gg/wXhwjCQ)\n\nredisbloom-py is a package that gives developers easy access to several probabilistic data structures. The package extends [redis-py](https://github.com/andymccurdy/redis-py)'s interface with RedisBloom's API.\n\n### Installation\n```\n$ pip install redisbloom\n```\n\n### Usage example\n\n```python\n# Using Bloom Filter\nfrom redisbloom.client import Client\nrb = Client()\nrb.bfCreate('bloom', 0.01, 1000)\nrb.bfAdd('bloom', 'foo')        # returns 1\nrb.bfAdd('bloom', 'foo')        # returns 0\nrb.bfExists('bloom', 'foo')     # returns 1\nrb.bfExists('bloom', 'noexist') # returns 0\n\n# Using Cuckoo Filter\nfrom redisbloom.client import Client\nrb = Client()\nrb.cfCreate('cuckoo', 1000)\nrb.cfAdd('cuckoo', 'filter')        # returns 1\nrb.cfAddNX('cuckoo', 'filter')      # returns 0\nrb.cfExists('cuckoo', 'filter')     # returns 1\nrb.cfExists('cuckoo', 'noexist')    # returns 0\n\n# Using Count-Min Sketch\nfrom redisbloom.client import Client\nrb = Client()\nrb.cmsInitByDim('dim', 1000, 5)\nrb.cmsIncrBy('dim', ['foo'], [5])\nrb.cmsIncrBy('dim', ['foo', 'bar'], [5, 15])\nrb.cmsQuery('dim', 'foo', 'bar')    # returns [10, 15]\n\n# Using Top-K\nfrom redisbloom.client import Client\nrb = Client()\nrb.topkReserve('topk', 3, 20, 3, 0.9)\nrb.topkAdd('topk', 'A', 'B', 'C', 'D', 'E', 'A', 'A', 'B',\n                   'C', 'G', 'D', 'B', 'D', 'A', 'E', 'E')\nrb.topkQuery('topk', 'A', 'B', 'C', 'D')    # returns [1, 1, 0, 1]\nrb.topkCount('topk', 'A', 'B', 'C', 'D')    # returns [4, 3, 2, 3]\nrb.topkList('topk')                         # returns ['A', 'B', 'E']\nrb.topkListWithCount('topk')                # returns ['A', 4, 'B', 3, 'E', 3]\n```\n\n### API\nFor complete documentation about RedisBloom's commands, refer to [RedisBloom's website](http://redisbloom.io).\n\n### License\n[BSD 3-Clause](https://github.com/RedisBloom/redisbloom-py/blob/master/LICENSE)\n\n### Development\n\n1. Create a virtualenv to manage your python dependencies, and ensure it's active.\n   ```virtualenv -v venv```\n2. Install [pypoetry](https://python-poetry.org/) to manage your dependencies.\n   ```pip install poetry```\n3. Install dependencies.\n   ```poetry install```\n\n[tox](https://tox.readthedocs.io/en/latest/) runs all tests as its default target. Running *tox* by itself will run unit tests. Ensure you have a running redis, with the module loaded.\n",
    'author': 'Redis',
    'author_email': 'oss@redis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
