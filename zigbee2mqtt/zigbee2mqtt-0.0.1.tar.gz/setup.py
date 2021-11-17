# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zigbee2mqtt']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'zigbee2mqtt',
    'version': '0.0.1',
    'description': 'Python client for Zigbee2MQTT.',
    'long_description': '# Python: Client for Zigbee2MQTT\n\n[![GitHub Release][releases-shield]][releases]\n[![Python Versions][python-versions-shield]][pypi]\n![Project Stage][project-stage-shield]\n![Project Maintenance][maintenance-shield]\n[![License][license-shield]](LICENSE.md)\n\n[![Build Status][build-shield]][build]\n[![Code Coverage][codecov-shield]][codecov]\n[![Code Quality][code-quality-shield]][code-quality]\n\n[![Sponsor Frenck via GitHub Sponsors][github-sponsors-shield]][github-sponsors]\n\n[![Support Frenck on Patreon][patreon-shield]][patreon]\n\nPython client for Zigbee2MQTT.\n\n## About\n\nIn progress Python client library for Zigbee2MQTT.\n\n## Installation\n\n```bash\npip install zigbee2mqtt\n```\n\n## Usage\n\n```python\n# TODO: Need example\n```\n\n## Changelog & Releases\n\nThis repository keeps a change log using [GitHub\'s releases][releases]\nfunctionality. The format of the log is based on\n[Keep a Changelog][keepchangelog].\n\nReleases are based on [Semantic Versioning][semver], and use the format\nof `MAJOR.MINOR.PATCH`. In a nutshell, the version will be incremented\nbased on the following:\n\n- `MAJOR`: Incompatible or major changes.\n- `MINOR`: Backwards-compatible new features and enhancements.\n- `PATCH`: Backwards-compatible bugfixes and package updates.\n\n## Contributing\n\nThis is an active open-source project. We are always open to people who want to\nuse the code or contribute to it.\n\nWe\'ve set up a separate document for our\n[contribution guidelines](CONTRIBUTING.md).\n\nThank you for being involved! :heart_eyes:\n\n## Setting up development environment\n\nThis Python project is fully managed using the [Poetry][poetry] dependency\nmanager. But also relies on the use of NodeJS for certain checks during\ndevelopment.\n\nYou need at least:\n\n- Python 3.8+\n- [Poetry][poetry-install]\n- NodeJS 14+ (including NPM)\n\nTo install all packages, including all development requirements:\n\n```bash\nnpm install\npoetry install\n```\n\nAs this repository uses the [pre-commit][pre-commit] framework, all changes\nare linted and tested with each commit. You can run all checks and tests\nmanually, using the following command:\n\n```bash\npoetry run pre-commit run --all-files\n```\n\nTo run just the Python tests:\n\n```bash\npoetry run pytest\n```\n\n## Authors & contributors\n\nThe original setup of this repository is by [Franck Nijhof][frenck].\n\nFor a full list of all authors and contributors,\ncheck [the contributor\'s page][contributors].\n\n## License\n\nMIT License\n\nCopyright (c) 2021 Franck Nijhof\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n[build-shield]: https://github.com/frenck/python-zigbee2mqtt/actions/workflows/tests.yaml/badge.svg\n[build]: https://github.com/frenck/python-zigbee2mqtt/actions/workflows/tests.yaml\n[code-quality-shield]: https://img.shields.io/lgtm/grade/python/g/frenck/python-zigbee2mqtt.svg?logo=lgtm&logoWidth=18\n[code-quality]: https://lgtm.com/projects/g/frenck/python-zigbee2mqtt/context:python\n[codecov-shield]: https://codecov.io/gh/frenck/python-zigbee2mqtt/branch/master/graph/badge.svg\n[codecov]: https://codecov.io/gh/frenck/python-zigbee2mqtt\n[contributors]: https://github.com/frenck/python-zigbee2mqtt/graphs/contributors\n[frenck]: https://github.com/frenck\n[github-sponsors-shield]: https://frenck.dev/wp-content/uploads/2019/12/github_sponsor.png\n[github-sponsors]: https://github.com/sponsors/frenck\n[keepchangelog]: http://keepachangelog.com/en/1.0.0/\n[license-shield]: https://img.shields.io/github/license/frenck/python-zigbee2mqtt.svg\n[maintenance-shield]: https://img.shields.io/maintenance/yes/2021.svg\n[patreon-shield]: https://frenck.dev/wp-content/uploads/2019/12/patreon.png\n[patreon]: https://www.patreon.com/frenck\n[poetry-install]: https://python-poetry.org/docs/#installation\n[poetry]: https://python-poetry.org\n[pre-commit]: https://pre-commit.com/\n[project-stage-shield]: https://img.shields.io/badge/Project%20Stage-Concept-red.svg\n[pypi]: https://pypi.org/project/zigbee2mqtt/\n[python-versions-shield]: https://img.shields.io/pypi/pyversions/zigbee2mqtt\n[releases-shield]: https://img.shields.io/github/release/frenck/python-zigbee2mqtt.svg\n[releases]: https://github.com/frenck/python-zigbee2mqtt/releases\n[semver]: http://semver.org/spec/v2.0.0.html\n',
    'author': 'Franck Nijhof',
    'author_email': 'opensource@frenck.dev',
    'maintainer': 'Franck Nijhof',
    'maintainer_email': 'opensource@frenck.dev',
    'url': 'https://github.com/frenck/python-zigbee2mqtt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
