from setuptools import find_packages,setup
from xes import version
import sys
if __name__=="__main__":
  sys.argv.append('sdist')
setup(
    name = 'h5gments',
    version = version.version,
    author = 'Ruoyu Wang',
    description = 'html5高亮库',
    packages = find_packages(),
    install_requires = ["pygments", "xes-lib", "pygame"],
    url = 'https://code.xueersi.com'
)