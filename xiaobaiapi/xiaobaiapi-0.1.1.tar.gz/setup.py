#! /usr/bin/env python
__script__ = 'setup.py'
__create__ = '2021/11/14 9:43 下午'
__author__ = 'Tser'
__email__ = '807447312@qq.com'


import setuptools
from xiaobaiapi.__version__ import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="xiaobaiapi",
    version=__version__,
    author="Tser",
    author_email="807447312@qq.com",
    description="xiaobaiapi 让接口测试起来更简单、人性化、更好玩  公众号：小白科技之窗",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/xiaobaikeji/xiaobaiapi",
    packages=setuptools.find_packages(),
    keywords="test api autoapi xiaobai xiaobaiapi httpclient",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "lxml",
        "jmespath",
        "requests",
    ],
)
'''
    package_data={
        'xiaobaiauto2': [
            'data/favicon.ico',
            'data/xiaobaiauto2.db',
            'test/runTestCase.bat',
            'utils/xiaobaiCaptcha.pyd',
            'utils/adb/adb.exe',
            'utils/adb/AdbWinApi.dll',
            'utils/adb/AdbWinUsbApi.dll'
        ],
    },
    entry_points={'console_scripts': [
        'xiaobaiauto2Timer = xiaobaiauto2.utils.xiaobaiauto2Timer:main',
        'xiaobaiauto2Api = xiaobaiauto2.utils.xiaobaiauto2Tools:cmd',
        'xiaobaiauto2Proxy = xiaobaiauto2.utils.xiaobaiauto2Proxy:cmd',
        'xiaobaiauto2App = xiaobaiauto2.utils.xiaobaiauto2App:adb_cmd',
    ]},
)
'''
#/usr/local/bin/python3.9 setup.py sdist bdist_wheel

#/usr/local/bin/python3.9 -m twine upload dist/*