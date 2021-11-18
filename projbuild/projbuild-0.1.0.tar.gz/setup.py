import setuptools

setuptools.setup(name="projbuild",
    version="0.1.0",
    description="a build system for c/c++ projects written in python",
    author="dskprt",
    url="https://github.com/dskprt/projbuild",
    packages=[ "projbuild" ],
    entry_points='''
        [console_scripts]
        projbuild=projbuild.main:main
    ''',
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent"
    ],
    install_requires=[ "click" ],
    python_requires=">=3.6")
