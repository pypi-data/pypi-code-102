import setuptools



setuptools.setup(
    name="pkg12345",
    version="0.0.2",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)