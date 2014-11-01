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

data = [
    ["data/weather.cap", "CAP1_1", "2014-05-10T22:00:00-06:00", "w-nws.webmaster@noaa.gov"],
    ["data/amber.atom", "ATOM", "2010-06-03T19:15:00-05:00", "KARO@CLETS.DOJ.DC.GOV"],
    ["data/australia.cap", "CAP1_2", "2011-10-05T23:04:00+10:00", "webmaster@rfs.nsw.gov.au"],
    ["data/earthquake.cap", "CAP1_1", "2010-08-31T00:09:25-05:00", "http://earthquake.usgs.gov/research/monitoring/anss/neic/"],
    ["data/earthquake-iso8859-1.cap", "CAP1_2", "2012-10-14T22:53:04+00:00", "http://earthquake.usgs.gov/research/monitoring/anss/neic/"],
    ["data/mexico.atom", "ATOM", "2014-10-31T21:15:00-06:00", "smn.cna.gob.mx"],
    ["data/taiwan.cap", "CAP1_2", "2014-05-14T20:10:00+08:00", "ddmt01@wra.gov.tw"],
]


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


class TestCAPParser_1_2(unittest.TestCase):
    def setUp(self):
        f = open('data/taiwan.cap', 'r').read()
        self.cap_object = CAPParser(f)

    def test_determine_cap_type(self):
        self.cap_object.determine_cap_type()
        self.assertEqual("CAP1_2", self.cap_object.cap_xml_type)

    def test_get_objectified_xml(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        children = objectified_xml.info.getchildren()
        self.assertIsNotNone(children)

    def test_parse_alert(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        alert_dict = self.cap_object.parse_alert(objectified_xml)
        self.assertEqual("2014-05-14T20:10:00+08:00", alert_dict['cap_sent'])

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual("ddmt01@wra.gov.tw", result[0]["cap_sender"])


class TestCAPParser_ATOM(unittest.TestCase):
    def setUp(self):
        f = open('data/amber.atom', 'r').read()
        self.cap_object = CAPParser(f)

    def test_determine_cap_type(self):
        self.cap_object.determine_cap_type()
        self.assertEqual("ATOM", self.cap_object.cap_xml_type)

    def test_get_objectified_xml(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        children = objectified_xml.entry.getchildren()
        self.assertIsNotNone(children)

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual("KARO@CLETS.DOJ.DC.GOV", result[0]["cap_sender"])


class TestSequence(unittest.TestCase):
    cap_object = None
    pass

def test_generator(filename, cap_xml_type, cap_sent, cap_sender):
    def test(self):
        f = open(filename, 'r').read()
        self.cap_object = CAPParser(f)
        self.cap_object.determine_cap_type()
        self.assertEqual(cap_xml_type, self.cap_object.cap_xml_type)

    def test_cap_load(self):
        f = open(filename, 'r').read()
        self.cap_object = CAPParser(f)
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual(cap_sender, result[0]["cap_sender"])
        self.assertEqual(cap_sent, result[0]['cap_sent'])

    def test_parse_alert(self):
        f = open(filename, 'r').read()
        self.cap_object = CAPParser(f)
        alert_list = self.cap_object.get_alert_list()
        alert = alert_list[0]
        alert_dict = self.cap_object.parse_alert(alert)
        self.assertEqual(cap_sent, alert_dict['cap_sent'])

    return test, test_cap_load, test_parse_alert


if __name__ == '__main__':
    from src.parsers import CAPParser

    # This creates dynamic test cases to test many files
    for t in data:
        test_name = 'test_%s' % t[0].split("/")[1].replace(".", "_")
        test, test_cap_load, test_parse_alert = test_generator(t[0], t[1], t[2], t[3])
        setattr(TestSequence, test_name, test)
        setattr(TestSequence, test_name + "cap_load", test_cap_load)
        setattr(TestSequence, test_name + "parse_alert", test_parse_alert)
    unittest.main()