#!/usr/bin/env python
"""
Build the capparselib module for parsing Common Alerting Protocol feeds.

"""
__author__ = 'kelvinn'
__email__ = 'kelvin@kelvinism.com'

from setuptools import setup

files = ["schema/*", "requirements-base.txt"]


def get_requirements(env):
    with open(u'src/requirements-{}.txt'.format(env)) as fp:
        return [x.strip() for x in fp.read().split('\n') if not x.startswith('#')]


install_requires = get_requirements('base')
tests_require = get_requirements('test')

setup(name="capparselib",
      version="0.6.7",
      description="A module to parse and standardise CAP feeds",
      long_description="This module provides the ability to parse Common Alerting Protocol (CAP) feeds and standardise"
                       " the resources into a dict, regardless if it was a 1.1 or 1.2 specification."
                       " Additional details can be found on the project's GitHub README: "
                       " https://github.com/kelvinn/capparselib",
      author="Kelvin Nicholson",
      author_email='kelvin@kelvinism.com',
      platforms=['posix'],
      install_requires=install_requires,
      extras_require={
          'tests': tests_require,
      },
      test_suite="tests",
      package_dir={'capparselib': 'src'},
      packages=['capparselib'],
      package_data={'capparselib': files},
      include_package_data=True,
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   ],
      )
