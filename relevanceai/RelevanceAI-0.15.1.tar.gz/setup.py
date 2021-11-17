import os

from setuptools import find_packages, setup


def read(rel_path):
    """Read lines from given file"""
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    """Read __version__ from given file"""
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError(f"Unable to find a valid __version__ string in {rel_path}.")


requirements = [
    "tqdm>=4.49.0",
    "pandas>=1.0.0",
    "loguru>=0.5.3",
    "document-utils>=1.3.0",
    "requests>=2.0.0",
    "numpy>=1.19.0",
]

excel_requirements = [
    "openpyxl>=3.0.9", 
    "fsspec>=2021.10.1"
]

vis_requirements = [
    "scikit-learn",
    "plotly>=5.3.1",
    "typing-extensions",
    "typeguard"
]

kmedoids = ["scikit-learn-extra"]
umap = ["umap-learn>=0.5.2"]
ivis_cpu = ["ivis[cpu]>=2.0.6"]
ivis_gpu = ["ivis[gpu]>=2.0.6"]

test_requirements =[
    "pytest",
    "pytest-dotenv",
    "pytest-cov",
    "pytest-mock",
    "mypy",
    "types-requests"
] + excel_requirements \
  + vis_requirements \
  + kmedoids \
  + umap \
  + ivis_cpu \
  + ivis_gpu

dev_requirements = [
    "autopep8",
    "pylint",
    "jupyter",
    "sphinx-rtd-theme>=0.5.0"
] + test_requirements



setup(
    name="RelevanceAI",
    version=get_version("relevanceai/__init__.py"),
    url="https://relevance.ai/",
    
    author="Relevance AI",
    author_email="dev@relevance.ai",
    long_description="",

    packages=find_packages(),

    setup_requires=["wheel"],
    install_requires=requirements,
    package_data={
        "": [
            "*.ini",
        ]
    },
    extras_require={
        "dev": dev_requirements,
        "excel": excel_requirements,
        "vis": vis_requirements,
        "tests": test_requirements,
        "notebook": ["jsonshower"] + vis_requirements,
        "kmedoids": kmedoids,
        "umap": umap,
        "ivis-cpu": ivis_cpu,
        "ivis-gpu": ivis_gpu,
    },
    python_requires=">=3.6",
    classifiers=[],
)
