import sys
from setuptools import setup, find_packages

from disca import VERSION

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md') as f:
    readme = f.read()

extras_require = {
    'voice': ['telecom-py==0.0.4'],
    'http': ['flask==2.0.2'],
    'yaml': ['pyyaml==6.0'],
    'music': ['youtube_dl==2021.6.6'],
    'performance': [
        'erlpack==0.3.3' if sys.version_info.major == 2 else 'earl-etf==2.1.2',
        'ujson==4.2.0',
        'wsaccel==0.6.3',
    ],
    'sharding': ['gipc==1.3.0'],
    'docs': ['biblio==0.0.4'],
}

setup(
    name='disca',
    author='py57',
    url='https://github.com/py57/disca',
    version=VERSION,
    packages=find_packages(include=['disca*']),
    license='MIT',
    description='A Python library for Discord',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    test_suite='tests',
    setup_requires=['pytest-runner==5.3.1'],
    tests_require=[
        'pytest==6.2.5',
        'pytest-benchmark==3.4.1',
        'flake8-tuple==0.4.1',
        'flake8-quotes==3.3.1',
        'flake8-comprehensions==3.7.0',
        'flake8-commas==2.1.0',
        'flake8-builtins==1.5.3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ])
