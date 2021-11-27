# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylicy']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pylicy',
    'version': '0.1.1',
    'description': 'Extensible and customizable policy definition and enforcement framework',
    'long_description': '# Pylicy\n\nAn customizable and extensible policy creation and enforcement framework.\n\n## Installation\n\n```\n$ pip install pylicy\n```\n\n## A Simple Example\n\nExamples can be found in the `examples/` directory.\n\n```python\nimport asyncio\nimport pylicy\n\n@pylicy.policy_checker(\'token_age_policy\')\nasync def my_policy(resource: pylicy.Resource, rule: pylicy.Rule) -> pylicy.PolicyDecision:\n    if resource.data[\'token_age\'] > 30:\n        return pylicy.PolicyDecision(\n            action=pylicy.PolicyDecisionAction.DENY,\n            reason="expired",\n            detail={\'age\': resource.data[\'token_age\']}\n        )\n    elif resource.data[\'token_age\'] > 20:\n        return pylicy.PolicyDecision(action=pylicy.PolicyDecisionAction.WARN)\n    else:\n        return pylicy.PolicyDecision(action=pylicy.PolicyDecisionAction.ALLOW)\n\npolicies = pylicy.Pylicy.from_rules([\n    pylicy.UserRule(\n        name=\'token_age\',\n        resources=[\'*_token*\'],\n        policies=[\'token_*\'],\n    )\n])\n\nresults = asyncio.run(policies.apply_all([\n    pylicy.Resource(id=\'my_ok_token\', data={\'token_age\': 10}),\n    pylicy.Resource(id=\'my_old_token\', data={\'token_age\': 21}),\n    pylicy.Resource(id=\'my_expired_token\', data={\'token_age\': 90})\n]))\n\nprint(results)\n```\n\n## License\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'uint0',
    'author_email': 'chen@czhou.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uint0/pylicy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
