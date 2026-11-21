"""Smoke test for an *installed* capparselib (not the source checkout).

Run from outside the repo so `src/` can't be picked up from the working
directory, which would mask packaging bugs such as
`ModuleNotFoundError: No module named 'src'` (issue #41).

Usage: python smoke_installed.py <path-to-cap-fixture>
"""
import sys

from capparselib.parsers import CAPParser


def main(fixture):
    with open(fixture, encoding='utf-8') as f:
        alerts = CAPParser(f.read()).as_dict()
    assert alerts, 'no alerts parsed from %s' % fixture
    print('OK: parsed %d alert(s)' % len(alerts))


if __name__ == '__main__':
    main(sys.argv[1])
