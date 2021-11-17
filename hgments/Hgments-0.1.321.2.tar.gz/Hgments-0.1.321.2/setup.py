import sys

if __name__=="__main__":
  sys.argv+=["sdist"]
from setuptools import find_packages,setup
from xes import version
setup(
    name = 'Hgments',
    version = str(version.version)+str(.2+1),
    author = 'Ruoyu Wang',
    description = 'html高亮库',
    packages = find_packages(),
    install_requires = ["pygments", "xes-lib", "pygame"],
    url = 'https://code.xueersi.com'
)