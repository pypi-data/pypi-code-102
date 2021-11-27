import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tsru",
    version="0.1.0",
    description="A simple library for various miscellaneous things",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/GaviTSRA/tsru",
    author="GaviTSRA",
    author_email="gavitsra@gmail.com",
    packages=find_packages(),
    #install_requires=[]
)