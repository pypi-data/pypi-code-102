"""Setup.py file"""
from setuptools import setup

__version__ = "v1.2"
__author__ = "Tyler Bruno"

with open("README.md", "r", encoding="utf-8") as file:
    README = file.read()

INSTALL_REQUIRES = ("pytest",)

setup(
    name="pytest-builtin-types",
    version=__version__,
    author=__author__,
    long_description=README,
    long_description_content_type="text/markdown",
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["builtin_types = pytest_builtin_types"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
    python_requires=">= 3.6.0",
    install_requires=INSTALL_REQUIRES,
    py_modules=["pytest_builtin_types"],
)
