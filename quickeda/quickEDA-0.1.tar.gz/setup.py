from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="quickEDA",
    version="0.1",
    description="All data analysis performed in single line of code",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Reshmamk1604/DSprojects/quickEDA",
    author="Reshma M K",
    author_email="mahdeeyafarha@gmail.com",
    keywords="EDA eda exploratory data analysis data preprocessing",
    license="MIT",
    packages=["quickEDA"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "edapython=quickEDA.__main__:main",]},
    include_package_data=True,
    zip_safe=False,
)