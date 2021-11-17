import pathlib
from setuptools import setup
#The directory containing this file
HERE = pathlib.Path(__file__).parent
#The text of the README file
README = (HERE / "README.md").read_text()
#This call to setup() does all the work
setup(
    name="dora_pktest",
    version="2.0.0",
    author="doranung",
    author_email="",
    description="Test packages",
    long_description=README,
    ong_description_content_type="text/markdown",
    url="https://github.com/doranung/dora_pktest",
    license="MIT",
     classifiers=[
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.7",
     ],
     packages=["dora_pktest_lib"],
     include_package_data=True,
     install_requires=[],
 )

