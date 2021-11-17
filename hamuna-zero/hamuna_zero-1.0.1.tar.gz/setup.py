import setuptools

setuptools.setup(
    name="hamuna_zero",
    version="1.0.1",
    author="O.Push",
    author_email="opush.developer@outlook.com",
    license="MIT",
    url="https://www.hamuna.club",
    description="Hamuna zero rpc framework based on pyzmq",
    long_description='support numpy data transfer',
    long_description_content_type="text/plain",
    packages=setuptools.find_packages(),
    package_dir={'':'.'},
    install_requires=['pyzmq', 'msgpack', 'typing-inspect', 'numpy', 'msgpack-numpy']
)
