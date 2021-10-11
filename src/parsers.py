#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    capparselib.CAPParser
    ~~~~~~~~~~~~~

    :copyright: Kelvin Nicholson (kelvin@kelvinism.com), see AUTHORS for more details
    :license: MOZILLA PUBLIC LICENSE (v1.1), see LICENSE for more details
"""
from __future__ import unicode_literals
import os
import logging
from lxml import objectify, etree

from src import cap_mappings

ATOM_URI = 'http://www.w3.org/2005/Atom'
CAP1_1_URN = 'urn:oasis:names:tc:emergency:cap:1.1'
CAP1_2_URN = 'urn:oasis:names:tc:emergency:cap:1.2'
EDXL_DE_URN = 'urn:oasis:names:tc:emergency:EDXL:DE:1.0'
XML_TYPE = None

CAPLIBRARY_PATH = os.path.realpath(os.path.dirname(__file__))

XML_TYPE_XSD_MAPPINGS = {
    'ATOM': 'schema/atom.xsd',
    'CAP1_2': 'schema/cap12_extended.xsd',
    'CAP1_1': 'schema/cap11_extended.xsd',
    'EDXL_DE': 'schema/edxl-de.xsd',
    'RSS': 'schema/rss-2_0.xsd',
}


class CAPParser(object):
    def __init__(self, raw_cap_xml=None, recover=False, mappings=cap_mappings.DEFAULT_CAP_MAPPINGS):
        self.xml = raw_cap_xml.encode('utf-8').strip() if raw_cap_xml is not None else None
        self.recover = recover
        self.mappings = mappings
        self.objectified_xml = None
        self.cap_xml_type = None
        self.alert_list = []
        self.load()

    def process_area(self, info_dict):
        new_area_list = []
        for area_obj in info_dict['area']:
            new_area_dict = {}
            if hasattr(area_obj, 'circle'):
                circles_list = []
                for circle in area_obj['circle']:
                    circles_list.append(circle)
                new_area_dict["circles"] = circles_list
            if hasattr(area_obj, 'polygon'):
                polygons_list = []
                for polygon in area_obj['polygon']:
                    polygons_list.append(polygon)
                new_area_dict["polygons"] = polygons_list
            if hasattr(area_obj, 'geocode'):
                geocode_list = []
                for geocode in area_obj['geocode']:
                    geocode_list.append({"valueName": geocode.valueName,
                                         "value": geocode.value})
                new_area_dict['geocodes'] = geocode_list
            new_area_dict['area_description'] = area_obj.areaDesc
            new_area_list.append(new_area_dict)
        info_dict['cap_area'] = new_area_list
        info_dict.pop('area')  # override the area value.
        return info_dict

    def process_event_code(self, info_dict):
        event_code_list = []
        for event_code in info_dict['event_code']:
            event_code_list.append({"valueName": event_code.valueName,
                                    "value": event_code.value})
        info_dict['cap_event_code'] = event_code_list
        info_dict.pop('event_code')
        return info_dict

    def process_parameter(self, info_dict):
        parameter_list = []
        for parameter in info_dict['parameter']:
            parameter_list.append({"valueName": parameter.valueName,
                                   "value": parameter.value})
        info_dict['cap_parameter'] = parameter_list
        info_dict.pop('parameter')
        return info_dict

    def process_resource(self, info_dict):
        resource_list = []
        for resource in info_dict['resource']:
            resource_list.append({"resourceDesc": resource.resourceDesc,
                                  "mimeType": resource.mimeType,
                                  "uri": resource.uri})
        info_dict['cap_resource'] = resource_list
        info_dict.pop('resource')
        return info_dict

    def parse_alert(self, alert):
        alert_dict = alert.__dict__

        # Standardise base alert keys across multiple CAP versions
        for alert_key in list(alert_dict):
            if alert_key in self.mappings:
                new_alert_key = self.mappings[alert_key]
                alert_dict[new_alert_key] = alert_dict.pop(alert_key)

        if 'info' in alert_dict.keys():
            info_item_list = []
            for info_item in alert.info:
                info_dict = info_item.__dict__

                # Standardise info keys across multiple CAP versions
                for info_key in list(info_dict):
                    if info_key in self.mappings:
                        new_info_key = self.mappings[info_key]
                        info_dict[new_info_key] = info_dict.pop(info_key)
                    else:
                        logging.info("Key not in self.mappings: %s" % info_key)

                if 'area' in info_dict.keys():
                    info_dict = self.process_area(info_dict)

                if 'event_code' in info_dict.keys():
                    info_dict = self.process_event_code(info_dict)

                if 'parameter' in info_dict.keys():
                    info_dict = self.process_parameter(info_dict)

                if 'resource' in info_dict.keys():
                    info_dict = self.process_resource(info_dict)

                info_item_list.append(info_dict)

            alert_dict['cap_info'] = info_item_list
            alert_dict.pop('info')
        return alert_dict

    def determine_cap_type(self):
        try:
            parser = etree.XMLParser(recover=self.recover, remove_blank_text=True)  # recovers from bad characters.
            tree = etree.fromstring(self.xml, parser)

        except ValueError:
            raise Exception("Invalid XML")

        ns_list = tree.nsmap.values()
        if ATOM_URI in ns_list:
            self.cap_xml_type = 'ATOM'
        elif CAP1_2_URN in ns_list:
            self.cap_xml_type = 'CAP1_2'
        elif CAP1_1_URN in ns_list:
            self.cap_xml_type = 'CAP1_1'
        elif EDXL_DE_URN in ns_list:
            self.cap_xml_type = 'EDXL_DE'
        else:  # probably RSS TODO Unfinished
            self.cap_xml_type = 'RSS'

    def dirty_invalid_xml_hacks(self):
        self.xml = bytes(self.xml).replace(b"<references />", b'')

    def get_objectified_xml(self):
        xsd_filename = XML_TYPE_XSD_MAPPINGS[self.cap_xml_type]
        with open(os.path.join(CAPLIBRARY_PATH, xsd_filename)) as f:
            doc = etree.parse(f)
            schema = etree.XMLSchema(doc)
            try:
                parser = objectify.makeparser(schema=schema, recover=self.recover, remove_blank_text=True)
                a = objectify.fromstring(self.xml, parser)
            except etree.XMLSyntaxError:
                raise Exception("Error objectifying XML")
        return a

    def get_alert_list(self):
        alerts = []
        objectified_xml = self.get_objectified_xml()
        if self.cap_xml_type == 'ATOM':
            for alert in objectified_xml.entry:
                alerts.append(alert.content.getchildren()[0])
        elif self.cap_xml_type == 'CAP1_1' or self.cap_xml_type == 'CAP1_2':
            alerts.append(objectified_xml)
        elif self.cap_xml_type == 'EDXL_DE':
            for obj in objectified_xml.contentObject:
                alert = obj.xmlContent.embeddedXMLContent.getchildren()[0]
                alerts.append(alert)
        return alerts

    def load(self):
        if self.xml:
            self.dirty_invalid_xml_hacks()
            self.determine_cap_type()
            for alert in self.get_alert_list():
                self.alert_list.append(self.parse_alert(alert))

    def as_dict(self):
        return self.alert_list
