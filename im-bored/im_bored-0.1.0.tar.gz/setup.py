from setuptools import setup, find_packages

VERSION = '0.1.0'

# Setting up
setup(
    name="im_bored",
    version=VERSION,
    description="A simple package that returns an interesting website in string.",
    author="Javier",
    author_email="javier.is.high@gmail.com",
    url="https://github.com/JavierDevs/Im-Bored-pypi",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'web','bored'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)