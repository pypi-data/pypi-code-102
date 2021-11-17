import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gitfunctions',
    version='0.0.2',
    url='https://github.com/strapbooll/git-functions',
    author='strapbooll',
    author_email='rximenez97@gmail.com',
    description='Lib for git functions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['GitPython'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)