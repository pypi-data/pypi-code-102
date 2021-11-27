import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Mentoss",
    version="0.0.1",
    author="Eniola Ajiboye",
    author_email="eajiboye@andrew.cmu.edu",
    description="Square and Cube any real number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eloyjaws/Mentoss",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
