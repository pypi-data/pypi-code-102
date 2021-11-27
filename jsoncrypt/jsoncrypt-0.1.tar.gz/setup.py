from distutils.core import setup
setup(
  name = 'jsoncrypt',         
  packages = ['jsoncrypt'],   
  version = '0.1',      
  license='MIT',        
  description = 'Encryption and Decryption of JSON files. Option of reading JSON files encrypted and adding a password.',
  author = 'Renne (GRC Algoritmos)',                   
  author_email = 'grc.algoritmos@gmail.com',      
  url = 'https://github.com/grc-algoritmos/jsoncrypt',   
  download_url = 'https://github.com/grc-algoritmos/jsoncrypt/archive/refs/tags/v_01.tar.gz',
  keywords = ['JSON', 'ENCRYPTION', 'DECRYPTION', 'ENCODE', 'OBFUSCATE'],   
  install_requires=[
          'hashlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
