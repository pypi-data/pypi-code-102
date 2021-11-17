from src.sageutils import __version__
from setuptools import find_packages, setup

long_description = "Sage common utilities library"


setup(
    name="sageutils",
    packages=find_packages(),
    scripts=["scripts/passutil"],
    version=__version__,
    description="Sage common utilities library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tony Tong",
    author_email="ttong@pro-ai.org",
    license="MIT",
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=[
        "cryptography",
        "fire",
    ],
)
