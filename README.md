# 🏷️ Chestny ZNAK Flow Validator

[![CI](https://github.com/ranas-mukminov/chestny-znak-flow-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/ranas-mukminov/chestny-znak-flow-validator/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

Open-source toolkit for validating the integrity of labeled-goods flows across the Russian "Честный ЗНАК" supply chain (producer → wholesaler → retail). This project helps businesses reconcile movement records, detect discrepancies, and generate human-friendly reports for regulatory compliance and dispute resolution.

## Overview

In Russia, labeled goods (pharmaceuticals, tobacco, footwear, etc.) must be tracked through the **Честный ЗНАК** (Chestny ZNAK) national tracking system. Companies at each stage — producers, wholesalers, retailers — export data from their ERP/WMS systems and must ensure consistency with the official GIS MT (State Information System for Monitoring).

This validator analyzes synthetic or anonymized exports (CSV/XLSX/XML) from different supply chain participants, builds a unified movement graph, and identifies:
- **Missing codes** reported in one system but absent in another
- **Status mismatches** (e.g., codes marked as "withdrawn" still appearing in retail inventory)
- **Quantity discrepancies** between batches and actual movements
- **Chain breaks** where custody transfers are not properly documented

The tool is designed for **compliance audits**, **internal reconciliation**, and **training/demo purposes** — it does NOT interact with the live GIS MT API.

## Key Features

- **Multi-format import**: Parse producer CSV, wholesaler XLSX, and retail XML exports with flexible column mapping profiles
- **Graph-based validation**: Build movement chains between entities and detect topology issues
- **Discrepancy detection**: Identify missing codes, status conflicts, quantity mismatches, and chain breaks
- **Human-readable reports**: Generate markdown or text summaries with actionable findings
- **AI-powered insights** (stub): Cluster problems, suggest claim drafts, and provide compliance recommendations
- **CLI and Web UI**: Run validations via command line (`typer`) or lightweight FastAPI web interface
- **Security-first**: Uses `defusedxml` for XML parsing and `pypdf>=3.9.0` to prevent DoS attacks
- **TDD ready**: Comprehensive unit and integration tests with CI/CD via GitHub Actions

## Architecture / Components

The project is organized into clean, modular packages:

```
cz_validator/
├── models.py              # Core domain models (Code, Movement, Batch, Discrepancy)
├── io_import/             # Format-specific importers (CSV, XLSX, XML) + mapping profiles
├── core/                  # Validation logic (status, quantity, consistency checkers + graph builder)
├── ai/                    # AI layer (report generation, claim suggestions, problem clustering)
├── cli/                   # Typer-based CLI application
└── webapp/                # FastAPI web interface (stub)
```

**Data flow**:
1. User provides producer/wholesaler/retail export files
2. Importers parse files → `Code`, `Movement`, `Batch` objects
3. Graph builder constructs supply chain topology
4. Checkers analyze graph → generate `Discrepancy` objects
5. AI layer produces human-friendly reports and claim drafts
6. Output to console, markdown file, or web UI

## Requirements

### System Requirements
- **OS**: Linux (Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+) or macOS
- **Python**: 3.11 or higher
- **RAM**: 512 MB minimum (2 GB recommended for large datasets)
- **Disk**: 100 MB for installation + space for input/output files

### Python Dependencies
- `typer>=0.9` — CLI framework
- `fastapi>=0.109` — Web API framework
- `pydantic>=1.10` — Data validation
- `openpyxl>=3.1` — Excel file parsing
- `PyYAML>=6.0` — Configuration files
- `pypdf>=3.9.0` — PDF parsing (security-hardened)
- `defusedxml>=0.7.1` — Safe XML parsing

### Network & Access
- No external API calls required (all processing is local)
- Internet access only needed for initial `pip install`

## Quick Start (TL;DR)

```bash
# 1. Clone the repository
git clone https://github.com/ranas-mukminov/chestny-znak-flow-validator.git
cd chestny-znak-flow-validator

# 2. Install dependencies
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install .

# 3. Run a sample validation
python -m cz_validator.cli.main validate \
  --producer examples/data/producer_export_sample.csv \
  --wholesaler examples/data/wholesaler_export_sample.xlsx \
  --retail examples/data/retail_export_sample.xml

# 4. Generate a human-readable report
echo '{"total_codes": 1500, "discrepancies": 23}' > /tmp/aggregates.json
python -m cz_validator.cli.main generate-report /tmp/aggregates.json
```

**Note**: The example files are synthetic and anonymized. Replace with your own exports for production use.

## Detailed Installation

### Install on Ubuntu / Debian

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3.11 (if not already installed)
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Clone repository
git clone https://github.com/ranas-mukminov/chestny-znak-flow-validator.git
cd chestny-znak-flow-validator

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install package
pip install --upgrade pip
pip install .

# Install development tools (optional)
pip install .[dev]
```

### Install on RHEL / Rocky Linux / AlmaLinux

```bash
# Enable EPEL and install Python 3.11
sudo dnf install -y epel-release
sudo dnf install -y python3.11 python3.11-pip

# Clone and install
git clone https://github.com/ranas-mukminov/chestny-znak-flow-validator.git
cd chestny-znak-flow-validator
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install .
```

### Install with Docker (optional)

```bash
# Build image
docker build -t cz-validator:latest .

# Run CLI command
docker run --rm -v $(pwd)/examples:/data cz-validator:latest \
  python -m cz_validator.cli.main validate \
  --producer /data/producer_export_sample.csv \
  --wholesaler /data/wholesaler_export_sample.xlsx \
  --retail /data/retail_export_sample.xml
```

**Note**: This repository does not currently include a Dockerfile. You can create one following standard Python best practices.

## Configuration

### Mapping Profiles

The validator uses **mapping profiles** to adapt to different ERP/WMS column naming conventions. Example profile in `cz_validator/io_import/mapping_profiles.py`:

```python
DEFAULT_CSV_MAPPING = {
    "code_column": "marking_code",      # Column name for labeling code
    "gtin_column": "gtin_14",           # GTIN identifier
    "batch_column": "batch_number",     # Batch/lot number
    "status_column": "current_status",  # Code status
    "owner_column": "owner_inn",        # Owner tax ID (INN)
}
```

To use a custom mapping, create a YAML config in `examples/configs/`:

```yaml
# examples/configs/my_erp_mapping.yaml
csv:
  code_column: "КодМаркировки"
  gtin_column: "GTIN"
  batch_column: "Партия"
  status_column: "Статус"
  owner_column: "ИНН_владельца"

xlsx:
  code_column: "Code"
  gtin_column: "Product_GTIN"
  # ... etc
```

Pass the config file to the importer in your code.

### Environment Variables

No environment variables are required for basic operation. Optional variables for AI features (when implemented):

```bash
# OpenAI API key for AI-powered report generation (future feature)
export OPENAI_API_KEY="sk-..."
# Anthropic API key (alternative)
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Usage & Common Tasks

### Run Validation via CLI

```bash
# Validate all three supply chain stages
python -m cz_validator.cli.main validate \
  --producer data/producer.csv \
  --wholesaler data/wholesaler.xlsx \
  --retail data/retail.xml

# Generate human-friendly report from aggregated results
python -m cz_validator.cli.main generate-report results/aggregates.json

# Export claim drafts (stub command)
python -m cz_validator.cli.main export-claims
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cz_validator --cov-report=html

# Run integration tests only
pytest tests/integration/

# Run linting and security checks
./scripts/lint.sh
./scripts/security_scan.sh
```

### Start Web UI (stub)

```bash
# Navigate to webapp module
python -m cz_validator.webapp.main

# Access UI at http://localhost:8000
# (Implementation is a placeholder; extend as needed)
```

### Import Custom Export Files

```python
from cz_validator.io_import.csv_importer import import_producer_csv
from cz_validator.io_import.xlsx_importer import import_wholesaler_xlsx
from cz_validator.io_import.xml_importer import import_retail_xml

# Import producer data
codes = import_producer_csv("my_producer_export.csv")

# Import wholesaler data
movements = import_wholesaler_xlsx("my_wholesaler_export.xlsx")

# Import retail data
batches = import_retail_xml("my_retail_export.xml")
```

## Update / Upgrade

### Update to Latest Version

```bash
cd chestny-znak-flow-validator
git pull origin main

# Reinstall with updated dependencies
source venv/bin/activate
pip install --upgrade .

# Run tests to verify
pytest
```

### Breaking Changes

- **v0.1.1**: Switched to `defusedxml` for XML parsing — update any custom XML importers accordingly
- **v0.1.1**: Requires `pypdf>=3.9.0` — older versions have DoS vulnerabilities

## Logs, Monitoring, Troubleshooting

### Logs

The validator outputs logs to `stderr` by default. Adjust logging level in your code:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

#### Issue: `ModuleNotFoundError: No module named 'cz_validator'`
**Solution**: Ensure you've activated the virtual environment and run `pip install .`

```bash
source venv/bin/activate
pip install .
```

#### Issue: `FileNotFoundError` when reading example files
**Solution**: Verify file paths are correct. Use absolute paths or run from repository root.

```bash
cd /path/to/chestny-znak-flow-validator
python -m cz_validator.cli.main validate --producer $(pwd)/examples/data/producer_export_sample.csv
```

#### Issue: `UnicodeDecodeError` when parsing CSV/XLSX
**Solution**: Ensure files are encoded in UTF-8 or specify encoding in importer.

#### Issue: Tests fail with `ImportError`
**Solution**: Install dev dependencies:

```bash
pip install .[dev]
```

#### Issue: Security scan reports outdated dependencies
**Solution**: Update dependencies to latest secure versions:

```bash
pip install --upgrade pypdf defusedxml
```

## Security Notes

### Production Deployment Checklist

- **Anonymize data**: Never use real labeling codes or personal data in testing
- **Input validation**: Validate all user-uploaded files for size limits, format, and content
- **Dependency scanning**: Run `./scripts/security_scan.sh` regularly and update vulnerable packages
- **Access control**: If deploying the web UI, use authentication (OAuth2, JWT) and HTTPS
- **Legal compliance**: Ensure your use of this tool complies with your contract with the Честный ЗНАК operator and Russian Federal Law 487-FZ

### Known Security Mitigations

- **XML bomb attacks**: Mitigated via `defusedxml` (v0.7.1+)
- **PDF DoS**: Mitigated via `pypdf>=3.9.0` (infinite loop fix)
- **CSV injection**: Importers do not execute formulas; safe for Excel preview

## Project Structure

```
chestny-znak-flow-validator/
├── cz_validator/           # Main package
│   ├── models.py           # Domain models (Code, Movement, Batch, Discrepancy)
│   ├── config.py           # Configuration constants
│   ├── io_import/          # Importers for CSV, XLSX, XML + mapping profiles
│   ├── core/               # Validation logic (status, quantity, consistency)
│   ├── ai/                 # AI-powered report generation and claim suggestions
│   ├── cli/                # Typer CLI application
│   └── webapp/             # FastAPI web interface (stub)
├── tests/                  # Unit and integration tests
│   ├── unit/
│   └── integration/
├── examples/               # Sample data and configs
│   ├── data/               # Synthetic CSV/XLSX/XML exports
│   ├── configs/            # Example mapping profiles
│   └── reports/            # Sample output reports
├── scripts/                # Development scripts (lint, test, security scan)
├── .github/workflows/      # CI/CD (pytest, CodeQL, security checks, Codex review)
├── pyproject.toml          # Project metadata and dependencies
├── LICENSE                 # Apache 2.0 license
├── LEGAL.md                # Legal disclaimers and compliance notes
├── SECURITY.md             # Security policy and vulnerability reporting
├── CONTRIBUTING.md         # Contribution guidelines and Codex Code Review setup
└── CHANGELOG.md            # Version history
```

## Roadmap / Plans

### Version 0.2.0 (Planned)
- Full AI integration with OpenAI/Anthropic for automatic claim generation
- Web UI enhancements (file upload, interactive graph visualization)
- Export to PDF and Excel formats
- Support for additional export formats (JSON, EDI)

### Version 0.3.0 (Planned)
- Multi-language support (UI in Russian and English)
- Performance optimization for datasets with >1M codes
- REST API for integration with external systems

See [GitHub Issues](https://github.com/ranas-mukminov/chestny-znak-flow-validator/issues) for open tasks and feature requests.

## Contributing

We welcome contributions from the community! Please follow these guidelines:

### How to Contribute

1. **Open an issue** to discuss bugs, features, or enhancements
2. **Fork the repository** and create a feature branch
3. **Write tests first** (TDD approach) before implementing new features
4. **Run all checks** before submitting a PR:
   ```bash
   ./scripts/lint.sh
   ./scripts/dev_run_all_tests.sh
   ./scripts/security_scan.sh
   ```
5. **Request Codex Code Review** by adding a comment `@codex review` to your PR
6. **Address review feedback** and ensure CI passes

### Code Style
- Follow **PEP 8** (enforced via linting)
- Use **type hints** for all functions and methods
- Keep modules focused: `io_import` for parsing, `core` for business logic, `ai` for AI features
- Write **docstrings** for public APIs (PEP 257)

### Setting Up Codex Code Review
1. Enable Codex Cloud for this repository in your GitHub settings
2. Turn on **Code review** feature in Codex Cloud dashboard
3. In PRs, trigger review manually with `@codex review` or enable auto-review
4. Address any security or logic regressions flagged by Codex

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions (in Russian).

## License

This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for full text.

You are free to use, modify, and distribute this software, provided you include the original copyright notice and license text.

## Author and Commercial Support

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)

For production-grade setup, custom integration with your ERP/WMS systems, compliance audits, and ongoing support, visit **[run-as-daemon.ru](https://run-as-daemon.ru)** (Russian) or contact the author via GitHub.

### Commercial Services
- Infrastructure audit and Честный ЗНАК compliance assessment
- Custom import adapters for 1C, SAP, or proprietary ERP systems
- Grafana/Prometheus monitoring setup for supply chain analytics
- DevOps/SRE consulting and CI/CD pipeline optimization

---

**Disclaimer**: This project is NOT an official product of Честный ZNAK or its operator. It does not use or distribute proprietary SDKs, closed documentation, or real labeling codes. All examples are synthetic and anonymized. Users are responsible for ensuring compliance with their contracts with the Честный ZNAK operator and Russian Federal Law 487-FZ. See [LEGAL.md](LEGAL.md) for details.
