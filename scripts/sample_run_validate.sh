#!/usr/bin/env bash
set -euo pipefail

python -m cz_validator.cli.main validate --producer examples/data/producer_export_sample.csv
