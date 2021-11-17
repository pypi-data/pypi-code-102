from setuptools import setup

setup(
	name = "height_selection_sim",
	packages = ['height_selection_sim'],
	version = "1.0.0",
	description = 'Simple Python program to simulate the effects of negative selection on a synthetic population of humans',
	author = "Elisha D.O. Roberson",
	author_email = 'dr.eli.roberson@gmail.com',
	url = 'https://github.com/RobersonLab/height_selection_sim',
	license = 'MIT',
	classifiers=[
	"Development Status :: 5 - Production/Stable",
	"Environment :: Console",
	"Intended Audience :: Science/Research",
	"Topic :: Scientific/Engineering :: Bio-Informatics",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.2",
	"Programming Language :: Python :: 3.3",
	"Programming Language :: Python :: 3.4",
	"Programming Language :: Python :: 3.5",
	"Programming Language :: Python :: 3.6",
	"Programming Language :: Python :: 3.7",
	"Programming Language :: Python :: 3.8",
	"Programming Language :: Python :: 3.9",
	"Programming Language :: Python :: 3.10"
	],
	keywords='natural selection simulator',
	install_requires = ['numpy', ],
	entry_points = {'console_scripts':["height_selection_sim = height_selection_sim.__main__:run"]}
)