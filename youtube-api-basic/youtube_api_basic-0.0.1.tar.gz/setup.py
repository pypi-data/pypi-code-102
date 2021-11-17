from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='youtube_api_basic',
  version='0.0.1',
  description='a very basic youtube api',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='khalil el ghoul',
  author_email='khalilelghoul01@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='youtube', 
  packages=find_packages(),
  install_requires=['requests', 'bs4'] 
)