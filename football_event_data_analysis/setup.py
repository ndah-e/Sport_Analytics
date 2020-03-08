from setuptools import setup, find_packages

setup(
    name='utils',
    version='0.0.1',
    packages=find_packages(include=['utils', 'utils.*']),
    install_requires=[
        'bs4==0.0.1',
        'numpy==1.17.3',
        'pandas==0.25.2',
        'dynaconf==2.2.0',

    ]
)