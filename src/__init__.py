# -*- coding: utf-8 -*-
__author__ = 'knichols'
name = "capparselib"

try:
    from ._version import version as __version__
except ImportError:
    __version__ = 'unknown'

__all__ = ['parsers', 'cap_mappings', 'schema']
