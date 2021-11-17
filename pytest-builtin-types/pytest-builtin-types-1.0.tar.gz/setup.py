"""Setup.py file"""
from setuptools import setup

INSTALL_REQUIRES = ("pytest",)

setup(
    name="pytest-builtin-types",
    version="v1.0",
    author="Tybruno",
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["builtin_types = pytest_builtin_types"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
    python_requires=">= 3.6.0",
    install_requires=INSTALL_REQUIRES,
    py_modules=["pytest_builtin_types"],
)
