import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyats_parser",
    version="1.0.0",
    description="Parse CLI output with pyATS/Genie Librairies",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rtrjl/pyats_parser",
    author="Rodolphe Trujillo",
    author_email="rodtruji@cisco.com",
    license="WTFPL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pyats_parser"],
    include_package_data=True,
    install_requires=["pyats", "genie"],

)
