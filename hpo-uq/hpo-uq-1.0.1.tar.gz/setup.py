from setuptools import setup,find_packages
from glob import glob

with open('README.rst', 'r') as f:
    longdesc = f.read()

setup(
    name="hpo-uq",
    version='1.0.1',
    description="Hyperparameter Optimization Tool using Surrogate Modeling and Uncertainty Quantification.",
    long_description=longdesc,
    long_description_content_type='text/x-rst',
    scripts = glob('bin/*'),
    author="Vincent Dumont",
    author_email="vincentdumont11@gmail.com",
    maintainer="Vincent Dumont",
    maintainer_email="vincentdumont11@gmail.com",
    url="https://hpo-uq.gitlab.io/hyppo",
    packages=find_packages(include=('hyppo*',)),
    project_urls={
        "Source Code": "https://gitlab.com/hpo-uq/hyppo",
    },
    install_requires=["deap","horovod","matplotlib","numpy","pandas","plotly","pyDOE","pyyaml","SALib","scipy","sklearn","tensorflow","torch"],
    classifiers=[
        'Intended Audience :: Science/Research',
        "License :: Other/Proprietary License",
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],

)
