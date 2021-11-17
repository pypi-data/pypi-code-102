from distutils.core import setup
import setuptools

def readme():
    with open('README.md', 'r', encoding="utf-8") as f:
        return f.read()

setup(
  name = 'copius_api',         # How you named your package folder (MyLib)
  packages = ['copius_api'],   # Chose the same as "name"
  version = '1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Transcription & orthography toolset',   # Give a short description about your library
  author = 'Viktor Martinović',                   # Type in your name
  author_email = 'viktormartin95@hotmail.com',      # Type in your E-Mail
  url = 'https://copius.eu/ortho.php',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/martino-vic/copius_api/archive/refs/tags/v1.1.tar.gz',    # I explain this later on
  keywords = ["api", "ipa", "transcription", "copius", "Volga-Kama"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'beautifulsoup4',
      ],
      
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.10',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Natural Language :: English',
    'Natural Language :: Russian',
  ],
  
  long_description=readme(),
  long_description_content_type='text/markdown'
)