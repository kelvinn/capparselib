#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    capparselib cap mappings
    ~~~~~~~~~~~~~

    :copyright: Kelvin Nicholson (kelvin@kelvinism.com), see AUTHORS for more details
    :license: MOZILLA PUBLIC LICENSE (v1.1), see LICENSE for more details
"""

# The dictionary keys is a list of attributes that are found in all CAP versions.
# The dictionary values are the default alert fields mappings for this library.
# Do not put event_code, eventCode, area, etc
DEFAULT_CAP_MAPPINGS = {
    'title': 'cap_headline',
    'summary': 'cap_description',
    'description': 'cap_description',
    'expires': 'cap_expires',
    'event': 'cap_event',
    'responseType': 'cap_response_type',
    'severity': 'cap_severity',
    'urgency': 'cap_urgency',
    'onset': 'cap_onset',
    'web': 'cap_link',
    'sent': 'cap_sent',
    'category': 'cap_category',
    'certainty': 'cap_certainty',
    'audience': 'cap_audience',
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
    'status': 'cap_status',
    'restriction': 'cap_restriction',
    'source': 'cap_source',
    'incidents': 'cap_incidents',
    'references': 'cap_references',
    'addresses': 'cap_addresses',
    'area': 'area',  # Leave this as 'area', as it get transformed.
    'eventCode': 'event_code',  # Leave this as 'area', as it get transformed.
    'parameter': 'parameter',  # Leave this as 'parameter', as it get transformed.
    'resource': 'resource',  # Leave this as 'parameter', as it get transformed.
}

# The dictionary keys is a list of attributes that are found in all CAP versions.
# The dictionary values are the alert fields mappings for CAP version 1.2
# Do not put event_code, eventCode, area, etc
CAP_1_2_MAPPINGS = {
    'title': 'headline',
    'summary': 'description',
    'description': 'description',
    'expires': 'expires',
    'event': 'event',
    'responseType': 'responseType',
    'severity': 'severity',
    'urgency': 'urgency',
    'onset': 'onset',
    'web': 'web',
    'sent': 'sent',
    'category': 'category',
    'certainty': 'certainty',
    'audience': 'audience',
    'headline': 'headline',
    'instruction': 'instruction',
    'language': 'language',
    'link': 'web',
    'author': 'sender',
    'areaDesc': 'areaDesc',
    'effective': 'effective',
    'sender': 'sender',
    'contact': 'contact',
    'senderName': 'senderName',
    'note': 'note',
    'code': 'code',
    'id': 'identifier',
    'identifier': 'identifier',
    'msgType': 'msgType',
    'scope': 'scope',
    'status': 'status',
    'restriction': 'restriction',
    'source': 'source',
    'incidents': 'incidents',
    'references': 'references',
    'addresses': 'addresses',
    'area': 'area',  # Leave this as 'area', as it get transformed.
    'eventCode': 'event_code',  # Leave this as 'area', as it get transformed.
    'parameter': 'parameter',  # Leave this as 'parameter', as it get transformed.
    'resource': 'resource',  # Leave this as 'parameter', as it get transformed.
}

# TODO, add mappings for CAP version 1.1
