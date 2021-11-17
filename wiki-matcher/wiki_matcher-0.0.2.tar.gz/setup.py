from setuptools import setup, find_packages

setup(
    name='wiki_matcher',
    maintainer='Tripp Weiner',
    url='https://github.com/TrippW/WikiMatcher',
    author='Tripp Weiner',
    description='Wiki Parsing and Loose Matching Aid',
    long_description='Wraps the reading, managing, caching, parsing, and matching of phrases found in specified html pages',
    keywords="parsing wiki loosematch db",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    project_urls={
        'Funding':'https://ko-fi.com/devtripp',
        'Source': 'https://github.com/TrippW/WikiMatcher'
    },
    install_requires=[
        'beautifulsoup4>=4.8.0',
        'requests>=2.25',
        'urllib3>=1.25',
		'strsimpy>=0.1.3'
    ],
	packages=['wiki_matcher'],
    version='0.0.2'
)
