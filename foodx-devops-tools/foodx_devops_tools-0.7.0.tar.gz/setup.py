#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['foodx_devops_tools',
 'foodx_devops_tools.azure',
 'foodx_devops_tools.azure.cloud',
 'foodx_devops_tools.deploy_me',
 'foodx_devops_tools.pipeline_config',
 'foodx_devops_tools.puff',
 'foodx_devops_tools.release_flow',
 'foodx_devops_tools.utilities']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles >=0.7.0',
 'ansible >=4.4.0, <5.0',
 'azure-devops >=6.0.0b4, <7.0',
 'click >=8.0.1, <9.0',
 'deepmerge >=0.3.0, <1.0',
 'jinja2 >=3.0.1, <4.0',
 'pydantic >=1.8.2, <2.0',
 'ruamel.yaml >=0.17.9, <1.0']

extras_require = \
{'dev': ['build_harness >=0.2.1, <1.0',
         'pre_commit >=2.7.1, <3.0',
         'pyjson5 >=1.5.2, <2.0',
         'types-aiofiles >= 0.1.9'],
 'doc': ['sphinx >=3.2.1, <4.0', 'sphinx_rtd_theme >=0.5.0, <1.0'],
 'test': ['asynctest >=0.13.0, <1.0',
          'pytest >=6.1.1, <7.0',
          'pytest-asyncio >=0.15.1, <1.0',
          'pytest-cov >=2.10.1, <3.0',
          'pytest-mock >=2.0.0, <3.0']}

entry_points = \
{'console_scripts': ['deploy-me = '
                     'foodx_devops_tools.deploy_me_entry:flit_entry',
                     'file-maintainer = '
                     'foodx_devops_tools.file_maintainer_entry:flit_entry',
                     'foodx-release-flow = '
                     'foodx_devops_tools.release_flow_entry:flit_entry',
                     'puff = foodx_devops_tools.puff_utility:entrypoint',
                     'validate-configuration = '
                     'foodx_devops_tools.validate_configuration:flit_entry']}

setup(name='foodx_devops_tools',
      version='0.7.0',
      description='Foodx DevOps pipeline utilities.',
      author='FoodX Technologies',
      author_email='support@foodxtech.com',
      url='https://github.com/Food-X-Technologies/foodx_devops_tools',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points=entry_points,
      python_requires='>=3.8',
     )
