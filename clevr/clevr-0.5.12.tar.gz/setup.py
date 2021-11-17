from setuptools import setup, find_packages
import setuptools


setup(
    name='clevr',
    version='0.5.12',
    description='Official Python SDK for Clevr.',
    long_description='Please visit https://beta.clevr-ai.com/docs for API examples and documentation.',
    package_dir={"": "clevr"},
    packages=setuptools.find_packages(where="clevr"),
    install_requires=[
             'Pillow>=7.1',
             'requests>=2.26'        
    ],
    license='MIT',
)