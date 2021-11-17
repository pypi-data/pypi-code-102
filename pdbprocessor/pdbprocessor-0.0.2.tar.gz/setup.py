import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdbprocessor",
    version="0.0.2",
    author="Igor Trujnara",
    author_email="itrujnara@wp.pl",
    description="Simple PDB data extraction program",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/igik20/pdbprocessor",
    project_urls={
        "Bug Tracker": "https://github.com/igik20/pdbprocessor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
