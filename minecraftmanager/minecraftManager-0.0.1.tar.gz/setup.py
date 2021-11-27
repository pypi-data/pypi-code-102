import setuptools
long_description = """# About


```py
from minecraftManager import *

manager = MinecraftRconManager(
  host="your.host",
  port=98712, #if port default(25565) use: #host="your.host"
                                           #password="rcon password"
  password="rcon password"
)
```
"""
setuptools.setup(
    name="minecraftManager", # Put your username here!
    version="0.0.1", # The version of your package!
    author="SScefaLI", # Your name here!
    author_email="birka11@list.ru", # Your e-mail here!
    description="Package to help creating and managing minecraft servers", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="", # Link your package website here! (most commonly a GitHub repo)
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'mctools'
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.8', # The version requirement for Python to run your package!
)