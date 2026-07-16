# Changelog

All notable changes to the OpenRefine Reconciliation Toolkit for Canadian Libraries will be documented in this file.

The project follows Semantic Versioning where practical.

---
## Version 1.1.0
**Release Date:** 2026-07-16

### Added

- Added support for the Library of Congress Suggest Service 2.0 API.
- Combined multiple Library of Congress search strategies (Suggest 2, Suggest, Did You Mean, and HTML search fallback) to improve reconciliation coverage.
- Added graceful error handling when the Library of Congress Did You Mean service is unavailable.

### Changed

- Improved reconciliation accuracy by preserving punctuation in Library of Congress authority headings.
- Standardized the Library of Congress reconciliation service to use `http://localhost:5000`.
- Improved duplicate detection by normalizing Library of Congress authority URIs returned by different search methods.
- Updated the reconciliation workflow to combine results from all enabled search methods, improving authority retrieval.
- Improved reconciliation success for complex Library of Congress subject headings through combined search strategies.

### Fixed

- Fixed compatibility issues caused by recent changes to the Library of Congress web services requiring HTTPS requests.
- Fixed failures when the Library of Congress Did You Mean service returned unavailable or malformed XML.


## Version 1.0.0
**Release Date:** 2026-07-07

### Added

- Initial release of the OpenRefine Reconciliation Toolkit for Canadian Libraries.
- Shared Python virtual environment for all included reconciliation services.
- Automated installation using `INSTALL_TOOLKIT.bat`.
- One-click startup of reconciliation services using `START_RECONCILIATION_SERVICES.bat`.
- Library of Congress reconciliation service supporting:
  - Library of Congress Name Authority File (LCNAF)
  - Library of Congress Subject Headings (LCSH)
- Canadian Subject Headings (CSH) reconciliation service built using `csv-reconcile`.
- Unified project documentation, installation instructions, troubleshooting guide, and toolkit structure documentation.
- Version tracking and release documentation.