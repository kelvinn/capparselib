#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" These are the tests for the the capparselib module. """

__author__ = 'kelvinn'
__version__ = '0.1'
__email__ = 'kelvin@kelvinism.com'

import os
import sys
import unittest

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(TEST_ROOT, os.pardir)
SRC_PATH = os.path.join(ROOT_PATH, 'src')

os.chdir(TEST_ROOT)
sys.path.insert(0, os.path.dirname(TEST_ROOT))
sys.path.insert(0, SRC_PATH)

