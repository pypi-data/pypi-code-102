from setuptools import setup

setup(
    name='stratz',
    packages=['stratz'],
    version='1.0',
    description='python lib for stratz.com',
    author='cxldxice',
    url='https://github.com/user/reponame',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    keywords=['stratz', 'dota', 'api'],
    install_requires=[
        'requests',
    ]
)
