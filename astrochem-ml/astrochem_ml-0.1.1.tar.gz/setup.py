# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astrochem_ml', 'astrochem_ml.smiles', 'astrochem_ml.smiles.tests']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0',
 'periodictable>=1.6.0,<2.0.0',
 'rdkit-pypi>=2021.9.2,<2022.0.0',
 'scikit-learn>=1.0.1,<2.0.0',
 'selfies>=2.0.0,<3.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'astrochem-ml',
    'version': '0.1.1',
    'description': 'Cheminformatics tools for astrochemistry',
    'long_description': '============\nAstrochem ML\n============\n\n\n.. image:: https://img.shields.io/pypi/v/astrochem_ml.svg\n        :target: https://pypi.python.org/pypi/astrochem_ml\n\n.. image:: https://img.shields.io/travis/laserkelvin/astrochem_ml.svg\n        :target: https://travis-ci.com/laserkelvin/astrochem_ml\n\n.. image:: https://readthedocs.org/projects/astrochem-ml/badge/?version=latest\n        :target: https://astrochem-ml.readthedocs.io/en/latest/?version=latest\n        :alt: Documentation Status\n\n\n\n\nDoing astrochemistry with robots.\n\nThe `astrochem_ml` package is designed for bringing accessible cheminformatics to\nastrochemical discovery. The main features, some of which are currently active\ndevelopment, are interfaces to common operations using RDKit that are relevant\nto astrochemistry, and pre-trained embedding models ready for machine learning\nprojects that combine molecules and astrophysics.\n\nThe plan is to deliver a general purpose library, in addition to providing a\ncommand line interface to several common tasks.\n\n\n* Free software: MIT license\n* Documentation: https://astrochem-ml.readthedocs.io.\n\nInstallation\n------------\n\nNot yet on PyPI, and so for now you can install `astrochem_ml` via:\n\n```pip install git+https://github.com/laserkelvin/astrochem_ml```\n\nFeatures\n--------\n\nMolecule generation\n===================\n\nA significant amount of functionality wraps the `rdkit` package, the main library\nfor doing cheminformatics in Python. For all molecule interactions, we go back\nand forth between the native `rdkit` objects and SMILES/SMARTS strings.\n\n* Exhaustive isotopologue generation in SMILES\n\n.. code-block:: python\n\n        >>> from astrochem_ml.smiles import isotopes\n        # exhaustively enumerate all possible combinations isotopologues\n        # user can set the threshold for natural abundance and whether\n        # to include hydrogens\n        >>> isotopes.generate_all_isos("c1ccccc1", explicit_h=False)\n        [\'c1[13cH]c[13cH][13cH][13cH]1\', ... \'c1ccccc1\', \'[13cH]1[13cH][13cH][13cH][13cH][13cH]1\',\'c1c[13cH][13cH][13cH]c1\']\n\n* Functional group substitutions\n\nReplace substructures with other ones in a tree data structure!\n\n.. code-block:: python\n\n        >>> from astrochem_ml.smiles import MoleculeGenerator\n        # randomly grow out possible structures starting from benzene,\n        # and iteratively replace structures with other functional groups\n        >>> benzene = MoleculeGenerator("c1ccccc1", substructs=["c", "cC#N", "cC=O", "cN"])\n        >>> benzene.grow_tree(50)\n        100%|██████████████████████████████████████████████████████████████████| 50/50 [00:00<00:00, 237.44it/s]\n        >>> print(benzene)\n        c1ccccc1\n        ├── Nc1ccccc1\n        ├── N#Cc1ccccc1\n        └── O=Cc1ccccc1\n        ├── Nc1ccccc1C=O\n        │   └── N#Cc1ccccc1C=O\n        ├── Nc1cccc(C=O)c1\n        │   ├── Nc1cccc(C=O)c1N\n        │   │   ├── Nc1c(C=O)ccc(C=O)c1N\n        │   │   ├── Nc1cc(C=O)cc(C=O)c1N\n        ...\n\nThis provides a high level interface to view every structure generated,\nand from which parent.\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Kelvin Lee',
    'author_email': 'kin.long.kelvin.lee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laserkelvin/astrochem_ml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
