# Changelog

## 0.1.1
### Security
- Upgraded to `pypdf>=3.9.0` to avoid an infinite-loop DoS when parsing crafted PDFs.
- Switched XML parsing to `defusedxml` to block entity-expansion attacks in retail import feeds.

## 0.1.0
- Initial repository skeleton with TDD-ready tests, CLI, FastAPI stub, importers, and validation core placeholders.
