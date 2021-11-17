import setuptools
from setuptools import find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(

    name="FDRParser",
    version="0.0.1",
    author="Makenna Kuzyk",
    author_email="",
    description="A python client library used to access the various libraries required for the FDR Parser script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "",
    
    install_requires=[
        "cycler==0.10.0" 
        "fonttools==4.28.1"
        "kiwisolver==1.3.2"  
        "matplotlib==3.5.0"  
        "numpy==1.21.3" 
        "packaging==21.2"   
        "Pillow==8.4.0"  
        "pyparsing==2.4.7"
        "python-dateuti==2.8.2"
        "six==1.16.0"
        "`tomli==1.2.2`"
    ],
    
    python_requires=">=3.10",
    packages=find_namespace_packages(','),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],

)