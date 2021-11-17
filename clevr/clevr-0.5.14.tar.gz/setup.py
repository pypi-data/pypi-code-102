import setuptools
from setuptools import setup, find_packages


setup(
    name='clevr',
    version='0.5.14',
    description='Official Python SDK for Clevr.',
    long_description='Please visit https://beta.clevr-ai.com/docs for API examples and documentation.',
    install_requires=[
             'Pillow>=7.1',
             'requests>=2.26'        
    ],
    license='MIT',
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"}
)


