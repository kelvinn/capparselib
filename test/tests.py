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

os.chdir(TEST_ROOT)
sys.path.insert(0, os.path.dirname(TEST_ROOT))


class TestCAPParser_1_1(unittest.TestCase):
    def setUp(self):
        f = open('data/weather.cap', 'r').read()
        self.cap_object = CAPParser(f)

    def test_determine_cap_type(self):
        self.cap_object.determine_cap_type()
        self.assertEqual("CAP1_1", self.cap_object.cap_xml_type)

    def test_get_objectified_xml(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        children = objectified_xml.info.getchildren()
        self.assertIsNotNone(children)

    def test_parse_alert(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        alert_dict = self.cap_object.parse_alert(objectified_xml)
        self.assertEqual("2014-05-10T22:00:00-06:00", alert_dict['cap_sent'])

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual("w-nws.webmaster@noaa.gov", result[0]["cap_sender"])

if __name__ == '__main__':
    from capparselib import CAPParser
    unittest.main()