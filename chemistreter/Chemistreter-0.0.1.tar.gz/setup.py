from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 8.1',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]

setup(
	name='Chemistreter',
	version='0.0.1',
	description='A helping mini library for Chemistry',
	long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
	url='',
	author='Mahdi Gasimov',
	author_email='mehditel75@gmail.com',
	license='MIT',
	classifiers=classifiers,
	keywords='function',
	packages=find_packages(),
	install_requires=['']
	)