import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

_REQUIRES = [
    "tensorflow-datasets>=4.2",
    "tensorflow>=2.1",
]

setup(
    name="tfds-aihub",
    version="0.1.0",
    author="Ukjae Jeong",
    author_email="jeongukjae@gmail.com",
    description="AIHub 데이터를 TFRecord 방식으로 가공하기 위한 프로젝트",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeongukjae/tfds-aihub",
    install_requires=_REQUIRES,
    keywords=["tensorflow", "machine learning", "dataset"],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
