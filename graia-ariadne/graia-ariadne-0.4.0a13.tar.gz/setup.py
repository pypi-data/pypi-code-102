# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia',
 'graia.ariadne',
 'graia.ariadne.event',
 'graia.ariadne.message',
 'graia.ariadne.message.parser']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'graia-broadcast>=0.12.1,!=0.14.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.2,<2.0.0',
 'typing-extensions>=3.10.0,<4.0.0',
 'yarl>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'graia-ariadne',
    'version': '0.4.0a13',
    'description': 'Anelegant mirai-api-http v2 Python SDK.',
    'long_description': '# Ariadne\n\n[![License](https://img.shields.io/github/license/GraiaProject/Ariadne)](https://github.com/GraiaProject/Ariadne/blob/master/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/graia-ariadne)](https://pypi.org/project/graia-ariadne)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/graia-ariadne)](https://www.python.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n---\n\n[API 文档](https://graiaproject.github.io/Ariadne/) 部署状态:\n[![PDoc Deploy](https://img.shields.io/github/deployments/GraiaProject/Ariadne/github-pages)](https://graiaproject.github.io/Ariadne/)\n\n[入门文档](https://graia.readthedocs.io/zh_CN/latest/)部署状态：\n[![Read The Docs Deploy](https://readthedocs.org/projects/graia/badge/?version=latest)](https://graia.readthedocs.io/zh_CN/latest/)\n\n一个适用于 [`mirai-api-http v2`](https://github.com/project-mirai/mirai-api-http) 的 Python SDK.\n\n**本项目适用于 mirai-api-http 2.0 以上版本**.\n\n目前仍处于开发阶段, 内部接口可能会有较大的变化.\n\n## 安装\n\n`poetry add graia-ariadne`\n\n或\n\n`pip install graia-ariadne`\n\n## 讨论\n\nQQ 交流群: [邀请链接](https://jq.qq.com/?_wv=1027&k=VXp6plBD)\n\n## 文档\n\n[API 文档](https://graiaproject.github.io/Ariadne/) [入门文档](https://graia.readthedocs.io/zh_CN/latest/)\n\n[鸣谢](https://graia.readthedocs.io/zh_CN/latest/appendix/credits)\n\n### 许可证\n\n[`GNU AGPLv3`](https://choosealicense.com/licenses/agpl-3.0/) 是本项目的开源许可证.\n',
    'author': 'BlueGlassBlock',
    'author_email': 'blueglassblock@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GraiaProject/Ariadne',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
