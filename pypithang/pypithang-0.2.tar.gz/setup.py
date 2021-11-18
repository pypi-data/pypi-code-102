from setuptools import setup, Extension
setup(
    name='pypithang',
    version='0.2',  # specified elsewhere
    packages=[''],
    package_dir={'': '.'},
#    include_package_data=True
   package_data={'': ['_example.so']},

)
