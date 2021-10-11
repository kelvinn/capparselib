#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" These are the tests for the the capparselib module. """

__author__ = 'kelvinn'
__email__ = 'kelvin@kelvinism.com'

import os
import sys
import unittest
import chardet
from io import open
from parameterized import parameterized
from src.parsers import CAPParser


TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(TEST_ROOT, os.pardir)

os.chdir(TEST_ROOT)
sys.path.insert(0, os.path.dirname(TEST_ROOT))

# filename, cap type, num alerts, sent time, sender

CAP_DATA_FILES = [
    ["resources/weather.cap", "CAP1_1", 1, "2014-05-10T22:00:00-06:00", "w-nws.webmaster@noaa.gov"],
    ["resources/NOAA_MultiplePolygons.txt", "CAP1_2", 1, "2020-08-26T04:14:00-05:00", "w-nws.webmaster@noaa.gov"],
    ["resources/amber.atom", "ATOM", 1, "2010-06-03T19:15:00-05:00", "KARO@CLETS.DOJ.DC.GOV"],
    ["resources/australia.cap", "CAP1_2", 1, "2011-10-05T23:04:00+10:00", "webmaster@rfs.nsw.gov.au"],
    # ["resources/us_nws_weather.atom", "ATOM", 2, "2014-05-10T22:00:00-06:00", "w-nws.webmaster@noaa.gov"],
    ["resources/earthquake.cap", "CAP1_1", 1, "2010-08-31T00:09:25-05:00",
     "http://earthquake.usgs.gov/research/monitoring/anss/neic/"],
    ["resources/earthquake-iso8859-1.cap", "CAP1_2", 1, "2012-10-14T22:53:04+00:00",
     "http://earthquake.usgs.gov/research/monitoring/anss/neic/"],
    ["resources/australia_bom.cap", "CAP1_2", 1, "2019-01-16T03:15:58+00:00", "CAP.Message@bom.gov.au"],
    # ["resources/sweden.cap", "CAP1_2", 1, "2018-10-12T11:05:18+02:00", "https://www.krisinformation.se/"],
    # ["resources/sweden.atom", "CAP1_2", 1, "2018-10-12T11:05:18+02:00", "https://www.krisinformation.se/"],
    ["resources/CanadaNaad.xml", "CAP1_2", 1, "2019-07-12T17:59:29-00:00", "cap-pac@canada.ca"],
    ["resources/mexico.xml", "CAP1_2", 1, "2018-10-20T07:15:00-05:00", "smn.cna.gob.mx"],
    ["resources/taiwan.cap", "CAP1_2", 1, "2014-05-14T20:10:00+08:00", "ddmt01@wra.gov.tw"],
    ["resources/ph.cap", "CAP1_2", 1, "2014-11-03T14:57:33+08:00", "PAGASA-DOST"],
    ["resources/wcatwc-warning.cap", "CAP1_2", 1, "2011-09-02T11:36:50-00:00",
     "http://newwcatwc.arh.noaa.gov/tsuPortal/"],
    ["resources/iceland_met_office.cap", "CAP1_2", 1, "2021-09-10T13:30:26-00:00", "IMO-Icelandic_Met_Office"]
]

CAP_DATA_FILES_NO_INFO = [
    ["resources/no_info_tag.cap", "CAP1_2", 1, "2016-02-25T12:47:09-08:00", "AtHoc"]
]


class TestCAPParser_1_1(unittest.TestCase):
    def setUp(self):
        with open('resources/weather.cap', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

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
        with open('resources/taiwan.cap', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

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

        info = alert_dict.get('cap_info')[0]
        self.assertEqual("Infra", info.get('cap_category'))
        self.assertEqual("Observed", info.get('cap_certainty'))
        self.assertEqual(u"水利署訊:明德水庫:洩洪中.影響範圍:後龍溪流域,鄉鎮:頭屋鄉,請及早應變.", info.get('cap_description'))
        self.assertEqual("2014-05-14T20:10:00+08:00", info.get('cap_effective'))
        self.assertEqual(u"水庫洩洪", info.get('cap_event'))
        self.assertEqual("2014-05-14T21:10:00+08:00", info.get('cap_expires'))
        self.assertEqual(u"明德水庫:洩洪中", info.get('cap_headline'))
        self.assertEqual("zh-tw", info.get('cap_language'))
        self.assertEqual("Monitor", info.get('cap_response_type'))
        self.assertEqual("Moderate", info.get('cap_severity'))
        self.assertEqual("Future", info.get('cap_urgency'))
        self.assertEqual("http://fhy2.wra.gov.tw/Pub_Web_2011/Page/Reservoir.aspx", info.get('cap_link'))
        self.assertEqual("profile:CAP-TWP:Event:1.0", info.get('cap_event_code')[0]['valueName'])
        self.assertEqual("ReservoirDis", info.get('cap_event_code')[0]['value'])
        self.assertEqual(u"水庫洩洪警戒", info.get('cap_parameter')[0]['value'])
        area = info.get('cap_area')[0]
        self.assertEqual(u"苗栗縣頭屋鄉", area['area_description'])
        self.assertEqual(1000512, area['geocodes'][0]['value'])

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual("ddmt01@wra.gov.tw", result[0]["cap_sender"])


class TestCAPParser_1_2_Canada(unittest.TestCase):
    def setUp(self):
        with open('resources/CanadaNaad.xml', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

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
        self.assertEqual("2019-07-12T17:59:29-00:00", alert_dict['cap_sent'])

        info = alert_dict.get('cap_info')[0]
        self.assertEqual("general public", info.get('cap_audience'))
        self.assertEqual("Possible", info.get('cap_certainty'))
        self.assertEqual("Monitor", info.get('cap_response_type'))
        self.assertEqual("Minor", info.get('cap_severity'))
        self.assertEqual("Future", info.get('cap_urgency'))
        self.assertEqual("profile:CAP-CP:Event:0.4", info.get('cap_event_code')[0]['valueName'])

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual("cap-pac@canada.ca", result[0]["cap_sender"])


class TestCAPParser_1_2_NOAA(unittest.TestCase):
    def setUp(self):
        with open('resources/NOAA_MultiplePolygons.txt', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

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
        self.assertEqual("2020-08-26T04:14:00-05:00", alert_dict['cap_sent'])

        info = alert_dict.get('cap_info')[0]
        self.assertEqual(None, info.get('cap_audience'))
        self.assertEqual("Likely", info.get('cap_certainty'))
        self.assertEqual("Avoid", info.get('cap_response_type'))
        self.assertEqual("Extreme", info.get('cap_severity'))
        self.assertEqual("Immediate", info.get('cap_urgency'))
        self.assertEqual("2020-08-26T04:14:00-05:00", info.get('cap_effective'))
        self.assertEqual("2020-08-26T04:14:10-05:00", info.get('cap_onset'))
        self.assertEqual("SAME", info.get('cap_event_code')[0]['valueName'])
        area = info.get("cap_area")[0]
        self.assertEqual(2, len(area.get("polygons")))
        self.assertEqual(
            "30.094,-92.619 30.091,-92.625 30.093,-92.623 30.094,-92.619",
            area.get("polygons")[0]
        )

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual("w-nws.webmaster@noaa.gov", result[0]["cap_sender"])


class TestCAPParser_ATOM(unittest.TestCase):
    def setUp(self):
        with open('resources/amber.atom', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

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
        with open('resources/bushfire_valid.edxlde', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual(9, len(result[0]))

    def test_as_dict(self):
        alerts = self.cap_object.as_dict()
        self.assertEqual(59, len(alerts))


class TestInvalid(unittest.TestCase):
    def setUp(self):
        self.data = None
        with open('resources/invalid.cap', 'br') as f:
            self.data = f.read()
            self.encoding = chardet.detect(self.data)['encoding']

    def test_invalid(self):
        self.assertRaises(Exception, CAPParser, self.data.decode(self.encoding))


class TestClass(unittest.TestCase):

    @parameterized.expand(CAP_DATA_FILES)
    def test_valid(self, filename, cap_xml_type, cap_alert_count, cap_sent, cap_sender):
        with open(filename, 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']

            # Can we even load the cap alert?
            self.cap_object = CAPParser(data.decode(encoding))
            self.cap_object.determine_cap_type()
            self.assertEqual(cap_xml_type, self.cap_object.cap_xml_type)

            # Did the CAP alert have a sender/sent?
            result = self.cap_object.alert_list
            self.assertEqual(cap_sender, result[0]["cap_sender"])
            self.assertEqual(cap_sent, result[0]['cap_sent'])
            self.assertEqual(cap_alert_count, len(result))

            # Now, can we parse the alerts?
            alert_list = self.cap_object.get_alert_list()
            alert = alert_list[0]
            alert_dict = self.cap_object.parse_alert(alert)
            self.assertEqual(cap_sent, alert_dict['cap_sent'])

            info_list = alert['info']
            self.assertIsNotNone(info_list)
