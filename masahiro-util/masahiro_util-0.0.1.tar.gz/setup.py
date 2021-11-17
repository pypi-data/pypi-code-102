import pathlib
from setuptools import setup
#The directory containing this file
HERE = pathlib.Path(__file__).parent
#The text of the README file
README = (HERE / "README.md").read_text()
#This call to setup() does all the work
setup(
    name="masahiro_util",
    version="0.0.1",
    author="javakung",
    author_email="gm.komyo@gmail.com",
    description="A simple package",
    long_description=README,
    ong_description_content_type="text/markdown",
    url="https://github.com/javakung/masahiro",
    license="MIT",
     classifiers=[
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.7",
     ],
     packages=["masahiro_lib"],
     include_package_data=True,
     install_requires=[],
 )

