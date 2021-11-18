from distutils.core import setup
setup (name = 'pypithang',
       version = '0.1',
       author = "Pradeesh",
       description = """Install precompiled extension""",
       py_modules = ["example"],
       packages=[''],
       package_dir={'': 'build'},
       package_data={'': ['*']},
       )
