#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Install the stackstatistics application. """
from setuptools import setup, find_packages
from stackstatistics.__version__ import __version__


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requires = [line.rstrip('\n') for line in f]

setup(
    name='stackstatistics',
    version=__version__,
    description='Stackstatistics application for simple analysis of data retrieved from the StackExchange API .',
    long_description=readme,
    author='Konstantinos Petsas',
    author_email='kons.petsas@gmail.com',
    license=license,
    packages=find_packages(exclude=('tests',)),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'statistics=stackstatistics:main'
        ]
    }
)
