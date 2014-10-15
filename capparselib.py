#!/usr/bin/env python
# coding: utf-8
"""
    capparselib.CAPParser
    ~~~~~~~~~~~~~

    This module parses and 'normalizes' alerts sent using the
    Common Alerting Protocol. It currently can handle XML in
    CAP1.1 and CAP1.2 format, and supports ATOM feeds.

    This module originally returned an 'Event' object, but now
    simply returns a dictionary. It currently does not lookup geocode
    items or any other items, but please make a request if you want
    sample code to do this (kelvin@kelvinism.com). There is almost
    no validation with parsing this - to be added shortly! Alert validation
    via signatures is also not supported, yet.

    Basic usage includes (from the source directory):

        >>> from capparselib import CAPParser
        >>> f = r'test/data/weather.cap'
        >>> src = open(f, 'r').read()
        >>> alert_list = CAPParser(src).as_dict()

    The CAPParser class returns a list of alerts, which are each a
    dictionary of items according to a hopefully logical mapping
    of fields. For instance, fields with names 'headline' (CAP1.2)
    and 'title' (CAP1.1) are both renamed to 'cap_headline'.
    Using the above basic usage example, you can then access
    fields as needed:

        >>> alert = alert_list[0]
        >>> alert['cap_sender']
            'w-nws.webmaster@noaa.gov'
        >>> alert.keys()
            ['cap_scope', 'cap_sender', 'cap_note', 'cap_status',
            'cap_id', 'cap_message_type', 'cap_sent', 'cap_info']
        >>> alert['cap_info'].keys()
            ['cap_area', 'cap_sender', 'cap_expires', 'cap_severity',
            'cap_event', 'cap_certainty', 'cap_urgency', 'cap_event_code',
            'cap_effective', 'cap_description', 'cap_parameter', 'cap_headline',
            'cap_instruction', 'cap_category']
        >>> alert['cap_info']['cap_severity']
            'Severe'

    If you want to try another CAP parser, take a look at 'cap-alerts',
    located at: https://code.google.com/p/cap-alerts/

    :copyright: Kelvin Nicholson (kelvin@kelvinism.com), see AUTHORS for more details
    :license: MOZILLA PUBLIC LICENSE (v1.1), see LICENSE for more details
"""

import os
from lxml import objectify, etree


ATOM_URI = 'http://www.w3.org/2005/Atom'
CAP1_1_URN = 'urn:oasis:names:tc:emergency:cap:1.1'
CAP1_2_URN = 'urn:oasis:names:tc:emergency:cap:1.2'
EDXL_DE_URN = 'urn:oasis:names:tc:emergency:EDXL:DE:1.0'
XML_TYPE = None

CAPLIBRARY_PATH = os.path.realpath(os.path.dirname(__file__))

# Do not put event_code, eventCode
CAP_MAPPINGS = {
    'title': 'cap_headline',
    'summary': 'cap_description',
    'description': 'cap_description',
    'expires': 'cap_expires',
    'responseType': 'cap_response_type',
    'severity': 'cap_severity',
    'urgency': 'cap_urgency',
    'onset': 'cap_effective',
    'web': 'cap_link',
    'category': 'cap_category',
    'certainty': 'cap_certainty',
    'event': 'cap_event',
    'headline': 'cap_headline',
    'instruction': 'cap_instruction',
    'language': 'cap_language',
    'link': 'cap_link',
    'author': 'cap_sender',
    'areaDesc': 'cap_area_description',
    'effective': 'cap_effective',
    'sender': 'cap_sender',
    'contact': 'cap_contact',
    'senderName': 'cap_sender_name',
    'note': 'cap_note',
    'code': 'cap_code',
    'id': 'cap_id',
    'identifier': 'cap_id',
    'msgType': 'cap_message_type',
    'scope': 'cap_scope',
    'sent': 'cap_sent',
    'status': 'cap_status',
    'restriction': 'cap_restriction',
    'source': 'cap_source',
    'incidents': 'cap_incidents',
    'references': 'cap_references',
    'addresses': 'cap_addresses',
}

XML_TYPE_XSD_MAPPINGS = {
    'ATOM': 'schema/atom.xsd',
    'CAP1_2': 'schema/cap12_extended.xsd',
    'CAP1_1': 'schema/cap11_extended.xsd',
    'EDXL_DE': 'schema/edxl-de.xsd',
    'RSS': 'schema/rss-2_0.xsd',
}


class CAPParser:
    def __init__(self, raw_cap_xml):
        self.xml = raw_cap_xml
        self.objectified_xml = None
        self.cap_xml_type = None
        self.alert_list = []
        self.load()

    def parse_alert(self, alert):
        alert_dict = alert.__dict__

        for alert_key in alert_dict.keys():
            if alert_key in CAP_MAPPINGS:
                new_alert_key = CAP_MAPPINGS[alert_key]
                alert_dict[new_alert_key] = alert_dict.pop(alert_key)

        info_item_list = []
        for info_item in alert.info:
            info_dict = info_item.__dict__

            for info_key in info_dict.keys():
                if info_key in CAP_MAPPINGS:
                    new_info_key = CAP_MAPPINGS[info_key]
                    info_dict[new_info_key] = unicode(info_dict.pop(info_key))

            if 'area' in info_dict.keys():
                new_area_list = []
                for area_obj in info_dict['area']:
                    new_area_dict = {}
                    if hasattr(area_obj, 'circle'):
                        new_area_dict['circle'] = info_dict['area'].circle
                    if hasattr(area_obj, 'polygon'):
                        new_area_dict['polygon'] = info_dict['area'].polygon
                    if hasattr(area_obj, 'geocode'):
                        #geocode_dict = {}
                        geocode_list = []
                        for geocode in area_obj['geocode']:
                            geocode_list.append({"valueName": unicode(geocode.valueName),
                                                 "value": unicode(geocode.value)})
                            #geocode_dict.update({geocode.valueName: geocode.value})
                        new_area_dict['geocodes'] = geocode_list
                    new_area_dict['area_description'] = unicode(area_obj.areaDesc)
                    new_area_list.append(new_area_dict)
                info_dict['cap_area'] = new_area_list
                info_dict.pop('area')  # override the area value.

            if 'eventCode' in info_dict.keys():
                event_code_list = []
                for event_code in info_dict['eventCode']:
                    event_code_list.append({"valueName": unicode(event_code.valueName),
                                            "value": unicode(event_code.value)})
                info_dict['cap_event_code'] = event_code_list
                info_dict.pop('eventCode')

            if 'parameter' in info_dict.keys():
                parameter_list = []
                for parameter in info_dict['parameter']:
                    parameter_list.append({"valueName": unicode(parameter.valueName),
                                           "value": unicode(parameter.value)})
                info_dict['cap_parameter'] = parameter_list
                info_dict.pop('parameter')

            if 'resource' in info_dict.keys():
                resource_list = []
                for resource in info_dict['resource']:
                    resource_list.append({"resourceDesc": unicode(resource.resourceDesc),
                                          "mimeType": unicode(resource.mimeType),
                                          "uri": resource.uri})
                info_dict['cap_resource'] = resource_list
                info_dict.pop('resource')

            info_item_list.append(info_dict)

        alert_dict['cap_info'] = info_item_list
        alert_dict.pop('info')
        return alert_dict

    def determine_cap_type(self):
        parser = etree.XMLParser(recover=True, remove_blank_text=True)  #recovers from bad characters.
        tree = etree.fromstring(self.xml, parser)

        #tree = etree.parse(filename, )
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

    def get_objectified_xml(self):
        xsd_filename = XML_TYPE_XSD_MAPPINGS[self.cap_xml_type]
        with open(os.path.join(CAPLIBRARY_PATH, xsd_filename)) as f:
            doc = etree.parse(f)
            schema = etree.XMLSchema(doc)
            parser = objectify.makeparser(schema=schema, recover=True, remove_blank_text=True)
            a = objectify.fromstring(self.xml, parser)
        return a

    def load(self):
        self.determine_cap_type()
        objectified_xml = self.get_objectified_xml()
        if self.cap_xml_type == 'ATOM':
            for alert in objectified_xml.entry.content.getchildren():
                self.alert_list.append(self.parse_alert(alert))
        elif self.cap_xml_type == 'CAP1.1' or self.cap_xml_type == 'CAP1.2':
            for alert in objectified_xml.info.getchildren():
                self.alert_list.append(self.parse_alert(alert))
        elif self.cap_xml_type == 'EDXL_DE':
            for alert in objectified_xml.contentObject.xmlContent.embeddedXMLContent.getchildren():
                self.alert_list.append(self.parse_alert(alert))
        else:
            self.alert_list.append(self.parse_alert(objectified_xml))

    def as_dict(self):
        return self.alert_list