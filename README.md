# OpenRefine Reconciliation Toolkit for Canadian Libraries

Making authority reconciliation in OpenRefine easier to install, maintain, and extend for Canadian libraries.

**Toolkit Version:** 1.0.0  
**Status:** Beta

Initial public release supporting Library of Congress and Canadian Subject Headings reconciliation services for OpenRefine.

## Overview

The OpenRefine Reconciliation Toolkit for Canadian Libraries is a collection of reconciliation services, utilities, and documentation designed to support authority control and metadata reconciliation workflows in OpenRefine.

The toolkit brings together multiple reconciliation services within a common installation, configuration, and documentation framework, making it easier to deploy, maintain, and extend OpenRefine reconciliation services across Canadian library environments.

## Features

- Library of Congress authority reconciliation (LCNAF and LCSH)
- Canadian Subject Headings reconciliation using csv-reconcile
- One-click startup of multiple reconciliation services
- Shared Python environment for simplified installation
- Extensible architecture for additional reconciliation services

## Current Components

The toolkit currently includes:

- Library of Congress Name Authority File (LCNAF) reconciliation service
- Library of Congress Subject Headings (LCSH) reconciliation service
- Canadian Subject Headings (CSH) reconciliation service
- Installation and startup tools
- Project documentation

## Intended Audience

The project is designed for metadata librarians, cataloguers, archivists, and repository managers who use OpenRefine to reconcile metadata against authority files and controlled vocabularies.

## System Requirements

The toolkit requires:

- OpenRefine
- Python 3.x
- Windows 10 or later
- Internet access during installation to download Python packages

OpenRefine must be installed separately. The toolkit provides reconciliation services that OpenRefine connects to; it does not install or launch OpenRefine.

## Installation

1. Download or copy the `reconciliation-toolkit` folder to your computer.

2. Open the folder.

3. Double-click:

   ```text
   INSTALL_TOOLKIT.bat
   ```
   
4. The installer will:

	- create a shared Python virtual environment.
	- install the required Python packages from `requirements.txt`.
	- prepare the toolkit for use.

5. When installation is complete, close the installer window.

> **Note**
>
> `INSTALL_TOOLKIT.bat` only needs to be run once unless the `venv` folder is deleted or `requirements.txt` is updated.


## Quick Start

1. Double-click:

```text
START_RECONCILIATION_SERVICES.bat
```

2. Two service windows will open:

- Library of Congress reconciliation service
- Canadian Subject Headings reconciliation service

Leave these command windows open while using OpenRefine.

3. Open OpenRefine.

4. The first time you use the toolkit, add the following reconciliation services in OpenRefine:

```text
http://localhost:5000/reconcile/LoC
```

```text
http://localhost:5001/reconcile
```

5. Use the Library of Congress service for:
	- LCNAF
	- LCSH

6. Use the CSH service for:

	- Canadian Subject Headings

When you are finished using OpenRefine, close the two reconciliation service command windows to stop the toolkit.

## Toolkit Structure

The toolkit is organized into the following directories and files:

```text
reconciliation-toolkit/
│
├── csh-service/
├── docs/
├── loc-service/
├── CHANGELOG.md
├── INSTALL_TOOLKIT.bat
├── LICENSE
├── README.md
├── requirements.txt
├── START_RECONCILIATION_SERVICES.bat
└── VERSION
```

After installation, the toolkit creates a shared Python virtual environment (`venv/`) in the root directory. This directory is generated automatically by `INSTALL_TOOLKIT.bat` and is not included in the repository.

### Directories

| Directory | Purpose |
|-----------|---------|
| `csh-service/` | Canadian Subject Headings (CSH) reconciliation service and supporting files. |
| `loc-service/` | Library of Congress reconciliation service (LCNAF and LCSH). |
| `docs/` | Additional project documentation. |

### Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, installation instructions, and user documentation. |
| `INSTALL_TOOLKIT.bat` | Creates the Python virtual environment and installs all required dependencies. |
| `START_RECONCILIATION_SERVICES.bat` | Starts all reconciliation services required by the toolkit. |
| `requirements.txt` | Lists the Python packages required to install and run the toolkit. |
| `CHANGELOG.md` | Version history and release notes. |
| `VERSION` | Current toolkit version. |
| `LICENSE` | Project license information. |

## Included Reconciliation Services

### Library of Congress Reconciliation Service

The toolkit includes a local instance of the Library of Congress OpenRefine reconciliation service.
The service queries Library of Congress authority data over the internet.

Supported vocabularies:

- Library of Congress Name Authority File (LCNAF)
- Library of Congress Subject Headings (LCSH)

Service URL:

```text
http://localhost:5000/reconcile/LoC
```

### Canadian Subject Headings (CSH) Reconciliation Service

The toolkit includes a local reconciliation service for Canadian Subject Headings built using `csv-reconcile`.
The service uses the included local reconciliation database and does not require an internet connection.

Service URL:

```text
http://localhost:5001/reconcile
```

The CSH reconciliation service supports searching authorized headings and associated search terms included in the distributed reconciliation database.


## Updating the Toolkit

Most users will not need to update the toolkit after installation. The following guidance explains when each component should be updated.

### Reinstalling Python Packages

Run `INSTALL_TOOLKIT.bat` again only if:

- the `venv` folder has been deleted,
- `requirements.txt` has been updated, or
- a newer version of the toolkit includes additional Python dependencies.

### Starting the Reconciliation Services

Run `START_RECONCILIATION_SERVICES.bat` each time you want to use the toolkit.

The reconciliation services are not started automatically when Windows or OpenRefine is launched.

### Updating the Canadian Subject Headings (CSH) Service

The CSH reconciliation database only needs to be rebuilt when the underlying reconciliation data changes.

Examples include:

- adding new subject headings,
- modifying existing reconciliation data,
- changing the reconciliation configuration (`csh.cfg`), or
- changing the reconciliation fields used to build the database.

When any of these changes occur, rebuild the database using `csv-reconcile init` before starting the service.

### Updating the Library of Congress Service

The Library of Congress reconciliation service does not require routine updates.

If the toolkit includes a newer version of the service, replace the contents of the `loc-service` directory with the updated files supplied with the toolkit release.

### Toolkit Updates

Future toolkit releases may include:

- additional reconciliation services,
- bug fixes,
- updated documentation,
- improvements to the installation and startup scripts.

Refer to `CHANGELOG.md` for a summary of changes between releases.

## Troubleshooting

### OpenRefine cannot connect to a reconciliation service

Ensure that:

- `START_RECONCILIATION_SERVICES.bat` has been run.
- The reconciliation service command windows remain open while using OpenRefine.
- The correct service URLs have been added to OpenRefine.

Library of Congress:

```text
http://localhost:5000/reconcile/LoC
```

Canadian Subject Headings:

```text
http://localhost:5001/reconcile
```

---

### Python is not found

If `INSTALL_TOOLKIT.bat` reports that Python cannot be found:

- Verify that Python 3.x is installed.
- Ensure that Python has been added to your system PATH.
- Restart the command prompt after installing Python.

---

### The toolkit will not install

If installation fails:

- Verify that you have an active internet connection.
- Ensure that `requirements.txt` is present in the toolkit directory.
- Run `INSTALL_TOOLKIT.bat` again.

---

### The CSH reconciliation service is out of date

If the underlying CSH reconciliation data has changed, rebuild the reconciliation database using `csv-reconcile init` before starting the service.

---

### The Library of Congress reconciliation service returns no results

Verify that:

- your internet connection is active,
- the Library of Congress website is available,
- the LoC reconciliation service is running.

---

### OpenRefine does not remember reconciliation services

OpenRefine stores configured reconciliation services in the user's profile directory.

If reconciliation services have been removed, add them again using the URLs listed above.

## Roadmap

Future planned additions include:

- Automated installation and startup
- Expanded documentation
- GitHub releases
- Additional reconciliation services
- Additional Canadian authority files
- Support for additional local reconciliation services
- Additional reconciliation services for Indigenous vocabularies

## License

This project is licensed under the MIT License.

Third-party software included with the toolkit remains subject to its original licensing terms. See the license files included with those components for details.

## Acknowledgements

This toolkit builds upon existing open-source projects, including:

- The Library of Congress OpenRefine reconciliation service
- csv-reconcile

The toolkit integrates these projects into a unified installation and documentation framework to simplify deployment, maintenance, and future extension for Canadian library environments.

The authors of the original projects deserve full credit for their respective software. This toolkit focuses on integration, configuration, documentation, and packaging rather than replacing or reimplementing their work.