import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seath",
    version="0.0.1",
    author="Matthew Seath",
    author_email="seathdesign@gmail.com",
    description="basic functions/tools for python coding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/seath",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/seath/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)