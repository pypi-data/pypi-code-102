import pathlib
from setuptools import setup
#The directory containing this file
HERE = pathlib.Path(__file__).parent
#The text of the README file
README = (HERE / "README.md").read_text()
#This call to setup() does all the work
setup(
    name = "yama_util",
    version = "0.0.0",
    author = "kaengyama",
    author_email = "pachitkaeng@gmail.com",
    description = "Sleepy cat all day and night",
    long_description = README,
    ong_description_content_type = "text/markdown",
    url = "https://github.com/yamato-kaeng/yama_util",
    license = "MIT",
     classifiers = [
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.7",
     ],
     packages = ["yama_util"], # Name 
     include_package_data = True,
     install_requires = [],
 )

