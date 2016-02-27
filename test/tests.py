#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" These are the tests for the the capparselib module. """
from StringIO import StringIO

__author__ = 'kelvinn'
__email__ = 'kelvin@kelvinism.com'

import os
import sys
import unittest
from StringIO import StringIO
from datetime import *
from dateutil.tz import *
import dateutil.parser
from lxml import etree

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(TEST_ROOT, os.pardir)

os.chdir(TEST_ROOT)
sys.path.insert(0, os.path.dirname(TEST_ROOT))

# filename, cap type, num alerts, sent time, sender

CAP_DATA_FILES = [
    ["data/weather.cap", "CAP1_1", 1, "2014-05-10T22:00:00-06:00", "w-nws.webmaster@noaa.gov"],
    ["data/amber.atom", "ATOM", 1, "2010-06-03T19:15:00-05:00", "KARO@CLETS.DOJ.DC.GOV"],
    ["data/australia.cap", "CAP1_2", 1, "2011-10-05T23:04:00+10:00", "webmaster@rfs.nsw.gov.au"],
    ["data/earthquake.cap", "CAP1_1", 1, "2010-08-31T00:09:25-05:00",
     "http://earthquake.usgs.gov/research/monitoring/anss/neic/"],
    ["data/earthquake-iso8859-1.cap", "CAP1_2", 1, "2012-10-14T22:53:04+00:00",
     "http://earthquake.usgs.gov/research/monitoring/anss/neic/"],
    ["data/mexico.atom", "ATOM", 469, "2014-10-31T21:15:00-06:00", "smn.cna.gob.mx"],
    ["data/taiwan.cap", "CAP1_2", 1, "2014-05-14T20:10:00+08:00", "ddmt01@wra.gov.tw"],
    ["data/ph.cap", "CAP1_2", 1, "2014-11-03T14:57:33+08:00", "PAGASA-DOST"],
    ["data/no_info_tag.cap", "CAP1_2", 1, "2016-02-25T12:47:09-08:00", "AtHoc"],
    ["data/wcatwc-warning.cap", "CAP1_2", 1, "2011-09-02T11:36:50-00:00", "http://newwcatwc.arh.noaa.gov/tsuPortal/"]
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


class TestCAPParser_EDXLDE(unittest.TestCase):
    def setUp(self):
        f = open('data/bushfire_valid.edxlde', 'r').read()
        self.cap_object = CAPParser(f)

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual(9, len(result[0]))

    def test_as_dict(self):
        alerts = self.cap_object.as_dict()
        self.assertEqual(59, len(alerts))

class TestInvalid(unittest.TestCase):
    def setUp(self):
        self.f = open('data/invalid.cap', 'r').read()

    def test_invalid(self):
        self.assertRaises(Exception, CAPParser, self.f)

class TestSerializer(unittest.TestCase):
    """
    This is a really big and ugly test, yet I wanted to create it to show that the autogenerated python classes
    work successfully. Additionally, it serves as an example on how to create a CAP 1.2 alert. The way this test
    works is that it first creates an alert, serilizes it to XML, and then deserializes to back to python objects. If
    there are any errors at all during this process it will fail miserably.

    """
    def test_serializer(self):

        # First create the alert object
        alert = serializer_1_2.alert()
        alert.code = ['urn:oasis:names:tc:emergency:cap:1.2:profile:CAP-AU:1.0']
        alert.identifier = 'tag:www.rfs.nsw.gov.au2011-10-06:40184'
        alert.msgType = 'Alert'
        alert.scope = 'Public'
        alert.sender = 'webmaster@rfs.nsw.gov.au'
        alert.sent = datetime.now(tzoffset("SYD", +36000)).replace(microsecond=0)
        alert.status = 'Actual'

        # Create a geocode object that will go into an area object
        geocode = serializer_1_2.geocode()
        geocode.value = u'AU-NSW'
        geocode.valueName = u'http://www.iso.org/iso/country_codes.html'

        # Create an area object to store the geocode object
        area = serializer_1_2.area()
        area.areaDesc = u'Yerong Creek Structure Fire'
        area.circle = ['-35.3888,147.0598 25.0']  # This requires a list
        area.geocode.append(geocode)

        # Create an event_code object to store codes
        event_code = serializer_1_2.eventCode()
        event_code.value = u'fire'
        event_code.valueName = u'https://govshare.gov.au/xmlui/handle/10772/6495'

        # Now create a parameter
        parameter = serializer_1_2.parameter()
        parameter.value = u'Forest'
        parameter.valueName = u'FuelType'

        # Create a resource object
        resource = serializer_1_2.resource()
        resource.mimeType = u'text/html'
        resource.resourceDesc = u'map'
        resource.uri = "http://www.rfs.nsw.gov.au/dsp_content.cfm?CAT_ID=683"

        # Now create an info object
        info = serializer_1_2.info()

        info.category = ['Fire']  # Category needs to be a list
        info.certainty = u'Observed'
        info.description = u'ALERT LEVEL: Not Applicable<br />LOCATION: 12 Cox Street, Yerong Creek<br />' \
            u'COUNCIL AREA: Lockhart<br />STATUS: Out of Control<br />TYPE: Structure fire ' \
            u'(A fire involving a residential, commercial or industrial building)<br />SIZE: 0 ha' \
            u'<br />RESPONSIBLE AGENCY: Rural Fire Service<br />UPDATED: 6 Oct 2011 10:04'
        info.effective = dateutil.parser.parse(u'2011-10-05T23:04:00+10:00')
        info.event = u'Fire'
        info.expires = dateutil.parser.parse(u'2011-10-06T23:04:00+10:00')
        info.headline = u'Yerong Creek Structure Fire'
        info.instruction = u'Not Applicable'
        info.language = u'en-AU'
        info.responseType = [u'Evacuate']  # responseType expects a list
        info.senderName = u'NSW Rural Fire Service'
        info.severity = u'Minor'
        info.urgency = u'Expected'
        info.parameter.append(parameter)
        info.resource.append(resource)
        info.eventCode.append(event_code)
        info.area.append(area)

        alert.info.append(info)

        xmlStr = StringIO()  # generateDS creates an 'export' function that is usually used to output to a file
        alert.export(xmlStr, 0, namespacedef_='xmlns:cap="urn:oasis:names:tc:emergency:cap:1.2"')
        output = xmlStr.getvalue()

        cap_object = CAPParser(output)
        cap_object.load()
        result = cap_object.alert_list
        self.assertEqual('webmaster@rfs.nsw.gov.au', result[0]["cap_sender"])


class TestSequence(unittest.TestCase):
    cap_object = None
    pass


def test_generator(filename, cap_xml_type, cap_alert_count, cap_sent, cap_sender):
    def test(self):
        f = open(filename, 'r').read()
        self.cap_object = CAPParser(f)
        self.cap_object.determine_cap_type()
        self.assertEqual(cap_xml_type, self.cap_object.cap_xml_type)

    def test_cap_load(self):
        f = open(filename, 'r').read()
        self.cap_object = CAPParser(f)
        #self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual(cap_sender, result[0]["cap_sender"])
        self.assertEqual(cap_sent, result[0]['cap_sent'])
        self.assertEqual(cap_alert_count, len(result))

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
    from src import serializer_1_2

    # This creates dynamic test cases to test many files
    for t in CAP_DATA_FILES:
        test_name = 'test_%s' % t[0].split("/")[1].replace(".", "_")
        test, test_cap_load, test_parse_alert = test_generator(t[0], t[1], t[2], t[3], t[4],)
        setattr(TestSequence, test_name, test)
        setattr(TestSequence, test_name + "_cap_load", test_cap_load)
        setattr(TestSequence, test_name + "_parse_alert", test_parse_alert)
    unittest.main()
