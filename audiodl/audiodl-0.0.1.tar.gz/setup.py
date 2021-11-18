from setuptools import setup, find_packages
import os

with open("README.md", encoding="utf8") as f:
    long_description = f.read()

# Setting up
setup(
    name="audiodl", 
    version="0.0.1",
    author="komal11lamba",
    author_email="komal11lamba@gmail.com",
    description="Audio Deep learning",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['librosa'],
    keywords=['audiodl','Audio Deep learning', 'Audio'],
    url='https://github.com/komal11lamba',
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    platforms=["any"],
    zip_safe=True,
)