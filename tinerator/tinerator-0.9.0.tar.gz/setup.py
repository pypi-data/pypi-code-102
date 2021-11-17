# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tinerator',
 'tinerator.examples',
 'tinerator.gis',
 'tinerator.meshing',
 'tinerator.tests',
 'tinerator.visualize']

package_data = \
{'': ['*'],
 'tinerator.examples': ['data/*',
                        'data/Borden/*',
                        'data/new_mexico/*',
                        'data/new_mexico/rasters/*',
                        'data/new_mexico/shapefiles/NHDFlowline/*',
                        'data/new_mexico/shapefiles/WBDHU12/*']}

install_requires = \
['Fiona>=1,<2',
 'MeshPy>=2020.0',
 'Shapely>=1,<2',
 'meshio>4.0.0',
 'numpy>=1,<2',
 'plotly>=5,<6',
 'pyproj>=3,<4',
 'pyshp>=2,<3',
 'pyvista>=0.30',
 'rich>=10,<11',
 'scipy>=1,<2',
 'snowy>=0.0.9,<0.0.10',
 'vtk>=9,<10']

setup_kwargs = {
    'name': 'tinerator',
    'version': '0.9.0',
    'description': 'Easy GIS-based 3D mesh generation',
    'long_description': None,
    'author': 'Daniel Livingston',
    'author_email': 'daniel.livingston@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
