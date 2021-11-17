import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jjckdockertool",
    version="1",
    author="曾章泉",
    author_email="2943917172@qq.com",
    description="自动部署容器环境",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.jjck.cn:2203/zengzhangquan/autodeployment",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

