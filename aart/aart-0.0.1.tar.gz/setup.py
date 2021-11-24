from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'AART'
LONG_DESCRIPTION = 'This blah blah'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="aart", 
        version=VERSION,
        author="Alejandro Cardenas-Avendano, Alex Lupsasca & Hengrui Zhu",
        author_email="<cardenas-avendano@princeton.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)