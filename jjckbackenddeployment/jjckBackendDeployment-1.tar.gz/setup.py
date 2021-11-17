import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jjckBackendDeployment",
    version="1",
    author="曾章泉",
    author_email="2943917172@qq.com",
    description="自动部署容器环境",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.jjck.cn:2203/zengzhangquan/autodeployment",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    package_data={
        # If any package contains *.txt files, include them:
        "": ["*.yaml"]
    }

)
