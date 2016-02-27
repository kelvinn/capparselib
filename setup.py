#!/usr/bin/env python
"""
Build the capparselib module for parsing Common Alerting Protocol feeds.

"""
__author__ = 'kelvinn'
__email__ = 'kelvin@kelvinism.com'

from setuptools import setup

files = ["schema/*"]

setup(name="capparselib",
    version="0.5.3",
    description="A module to parse and standardise CAP feeds",
    long_description="This module provides the ability to parse Common Alerting Protocol (CAP) feeds and standardise"
                     " the data into a dict, regardless if it was a 1.1 or 1.2 specification."
                     " Additional details can be found on the project's GitHub README: https://github.com/kelvinn/capparselib",
    author="Kelvin Nicholson",
    author_email='kelvin@kelvinism.com',
    platforms = ['any'],
    install_requires=["lxml", "python-dateutil"],
    package_dir = {'capparselib': 'src'},
    packages = ['capparselib'],
    package_data = {'capparselib' : files },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ],
)
