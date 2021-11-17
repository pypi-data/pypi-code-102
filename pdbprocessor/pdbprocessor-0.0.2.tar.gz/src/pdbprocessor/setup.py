from setuptools import setup
setup(
    name='pdbprocessor',
    version='0.0.2',
    entry_points={
        'console_scripts': [
            'pdbprocessor=pdbprocessor:main'
        ]
    }
)
