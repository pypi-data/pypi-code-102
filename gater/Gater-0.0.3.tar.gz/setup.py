from setuptools import setup

setup(
    name="Gater",
    version="0.0.3",
    author="turkey sui",
    author_email="suiminyan@gmail.com",
    url='',
    description="gate.io history data downloader",
    packages=['Gater'],
    install_requires=[
        "pandas",
        "urllib",
        "gzip",
        "io",
        "time"
    ]
)