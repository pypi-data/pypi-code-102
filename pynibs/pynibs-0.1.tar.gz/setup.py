from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import sys


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        check_call(sys.path[0] + "/postinstall/develop.py")
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        check_call(sys.path[0] + "/postinstall/install.py")
        install.run(self)


setup(name='pynibs',
      version='0.1',
      description='A toolbox to prepare and analyse non-invasive brain stimulation experiments (NIBS).',
      author='Konstantin Weise',
      author_email='kweise@cbs.mpg.de',
      keywords=['NIBS', 'non-invasive brain stimulation', 'TMS', 'FEM'],
      download_url='https://gitlab.gwdg.de/tms-localization/pynibs/-/archive/v0.1/pynibs-v0.1.tar.gz',

      license='GPL3',
      packages=['pynibs',
                'pynibs.exp',
                'pynibs.models',
                'pynibs.util',
                'pynibs.pckg'],
      install_requires=['dill',
                        'h5py',
                        'lmfit',
                        'matplotlib',
                        'numpy',
                        'nibabel',
                        'pandas',
                        'pygpc',
                        'pyyaml',
                        'scipy',
                        'scikit-learn',
                        'packaging',
                        'lxml',
                        'tables',
                        'tqdm',
                        'pillow',
                        'fslpy',
                        'mkl',
                        'trimesh',
                        'fmm3dpy',
                        'tvb-gdist'],
      zip_safe=False)
