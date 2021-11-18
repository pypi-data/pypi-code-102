from setuptools import setup, find_packages


setup(
    name='test_model_hv',
    version='0.0.1',
    license='MIT',
    author="Vishnu M Harshvardhan",
    author_email='m.vishnu701@gmail.com, reachhvg@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='',
    py_modules=['astromer'],
    install_requires=[
        'scikit-learn',
        'pandas',
        'joblib',
        'tqdm',
        'graphviz',
        'pydot',
        'scikit-learn',
        'seaborn',
        'googledrivedownloader',
        'dask[dataframe]',
        'optuna',
      ],

)