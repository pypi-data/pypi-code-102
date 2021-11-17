# import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

# setuptools.setup(
#     name="longbug_util",
#     version="0.0.1",
#     author="c-tawayip",
#     author_email="piyawatchuangkrud@gmail.com",
#     description="A simple Longbug package",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/pypa/sampleproject",
#     # project_urls={
#     #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
#     # },
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.7",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     package_dir={"": "src"},
#     packages=setuptools.find_packages(where="src"),
#     python_requires=">=3.7",
# )

import pathlib
from setuptools import setup
#The directory containing this file
HERE = pathlib.Path(__file__).parent
#The text of the README file
README = (HERE / "README.md").read_text()
#This call to setup() does all the work
setup(
    name="longbug_util",
    version="0.0.1",
    author="c-tawayip",
    author_email="piyawatchuangkrud@gmail.com",
    description="A simple Longbug package",
    long_description=README,
    ong_description_content_type="text/markdown",
    url="https://github.com/c-tawayip/longbug_util",
    license="MIT",
     classifiers=[
         "License :: OSI Approved :: MIT License",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.7",
     ],
     packages=["longbug_util"],
     include_package_data=True,
     install_requires=[],
    #  entry_points={
    #      "console_scripts": [
    #          "mcs=samplepackage.__main__:main",
    #      ]
    #  },
 )

