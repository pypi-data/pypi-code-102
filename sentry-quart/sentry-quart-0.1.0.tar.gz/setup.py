# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentry_quart']

package_data = \
{'': ['*']}

install_requires = \
['sentry-sdk>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'sentry-quart',
    'version': '0.1.0',
    'description': 'Sentry middleware for quart',
    'long_description': '# sentry-quart\nThe sentry middleware for quart\n\nSentry-asgi can\'t not collect the information like Flask\n\n## How to install\n\n```\npip install sentry-quart\n\n```\n\n## How to use\n\n```\nfrom quart import Quart\nfrom sentry_quart import QuartMiddleware\n\napp = Quart(__name__)\nhost = "https://xxxx.com/v1"\napp.asgi_app = QuartMiddleware(app, host)._run_asgi3\nsentry_sdk.init(traces_sample_rate=1)\n```\n',
    'author': 'hs',
    'author_email': 'huangxiaohen2738@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ponytailer/sentry-quart.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
