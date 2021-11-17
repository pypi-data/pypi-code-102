import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.txt").read_text()

# This call to setup() does all the work
setup(
    name="numpyDealer",
    version="1.0.2",
    description="Playing cards in numpy decks.",
    long_description=README,
    long_description_content_type="text/plain",
    author="Ethan Griffin",
    author_email="ethbgriffin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["numpyDealer"],
    include_package_data=True,
    install_requires=["numpy"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)