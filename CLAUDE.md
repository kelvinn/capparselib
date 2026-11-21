# CLAUDE.md

## Overview

`capparselib` is a small Python library (published on PyPI) that parses Common Alerting Protocol (CAP 1.1/1.2) XML, Atom feeds containing CAP alerts, and EDXL-DE wrappers, and normalises them into a list of dicts with `cap_*` keys. Built on `lxml.objectify` with XSD validation.

## Layout

- `src/` is the package, installed as `capparselib` (`package_dir={'capparselib': 'src'}` in `setup.py`). Note the split: **the code imports itself as `src.*`** (`from src import cap_mappings`, tests use `from src.parsers import CAPParser`), but users import `capparselib.*`. Keep that in mind when adding imports.
- `src/parsers.py`: `CAPParser`. Flow in `load()`: `dirty_invalid_xml_hacks` → `determine_cap_type` (sniffs XML namespaces: ATOM / CAP1_2 / CAP1_1 / EDXL_DE / else RSS) → `get_objectified_xml` (validates against the XSD in `XML_TYPE_XSD_MAPPINGS`) → `get_alert_list` (extracts alert elements per type) → `parse_alert` (renames keys via mappings, then `process_area/event_code/parameter/resource` for nested structures). Results come from `as_dict()`.
- `src/cap_mappings.py`: `DEFAULT_CAP_MAPPINGS` (CAP1.1 and 1.2 source names → `cap_*` names) and `CAP_1_2_MAPPINGS`. Passed via `CAPParser(src, mappings=...)`. Nested elements (`area`, `eventCode`, etc.) are handled in code, not in the mappings.
- `src/schema/`: XSDs bundled as package data. The `*_extended.xsd` variants are the ones actually used for validation.
- `tests/tests.py`: single unittest module using `parameterized`; fixtures in `tests/resources/` (real-world CAP/Atom/RSS/EDXL samples, including invalid and signed ones). Tests `chdir` to `tests/`.
- `tasks.py`: `invoke` tasks (`clean`, `build`, `package`, `install`, `unit`, `flake8`, `upload`, `upload_test`).

## Commands

```bash
pip install -r src/requirements-base.txt -r src/requirements-test.txt   # runtime + test deps
python -m unittest tests.tests          # run tests
inv unit                                   # tests under coverage
inv flake8                                 # lint (same as CI)
```

Runtime deps are in `src/requirements-base.txt` (`lxml`, `python-dateutil`, `chardet`) and are read by `setup.py`. Update there, not in `setup.py`.

## Conventions and gotchas

- Style: flake8, max line length 160 (`tox.ini` and `inv flake8`), max complexity 10.
- CI (`.github/workflows/python-package.yml`) tests Python 3.10–3.13 and publishes to PyPI on a GitHub release. Releases require bumping `version` in `setup.py`. Avoid syntax newer than 3.10.
- `parse_alert` mutates the lxml objects' `__dict__` in place; keys not in the mapping are logged at info level and left unmapped in info dicts.
- Errors are raised as bare `Exception("Invalid XML")` / `Exception("Error objectifying XML")`; tests may rely on this.
- `recover=True` makes lxml tolerate bad XML; `dirty_invalid_xml_hacks` strips `<references />` which breaks validation.
- RSS is the fallback type in `determine_cap_type` and is marked unfinished (`get_alert_list` returns nothing for it).
- When adding support for a new feed/profile, add a fixture to `tests/resources/` and a case in `tests/tests.py`.
- `__init__.py` at repo root and in `src/` is intentional for the packaging layout.
