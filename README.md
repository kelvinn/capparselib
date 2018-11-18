# capparselib

[![Coverage Status](https://coveralls.io/repos/github/kelvinn/capparselib/badge.svg?branch=master)](https://coveralls.io/github/kelvinn/capparselib?branch=master)
[![Build Status](https://travis-ci.org/kelvinn/capparselib.svg)](https://travis-ci.org/kelvinn/capparselib)

This module parses and 'normalizes' alerts sent using the
Common Alerting Protocol. It currently can handle XML in
CAP1.1 and CAP1.2 format, and supports ATOM feeds.

This module originally returned an 'Event' object, but now
simply returns a dictionary. It currently does not lookup geocode
items or any other items, but please make a request if you want
sample code to do this (kelvin@kelvinism.com). Alert validation
via signatures is also not supported, yet.

## Installation

You can install it from source with:

    $ python setup.py install

You can also install it directly with pip:

    $ pip install capparselib

## Usage

Basic usage includes (from the source directory):

    >>> from capparselib.parsers import CAPParser
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

Or RCAP, for Ruby, located here: https://github.com/farrel/RCAP
