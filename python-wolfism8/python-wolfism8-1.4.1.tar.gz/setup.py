""" setup for creating pypi package """
from pathlib import Path
from setuptools import find_packages, setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "1.4.1"

setup(
    name="python-wolfism8",
    version=VERSION,
    author="marcschmiedchen",
    author_email="marc.schmiedchen@protonmail.com",
    description="Get data from wolf heating system via ISM8",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["test.*", "test"]),
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
)
