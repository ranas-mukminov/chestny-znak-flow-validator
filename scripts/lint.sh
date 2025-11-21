#!/usr/bin/env bash
set -euo pipefail

if command -v ruff >/dev/null 2>&1; then
  ruff check .
else
  echo "ruff not installed, skipping"
fi

if command -v mypy >/dev/null 2>&1; then
  mypy cz_validator || true
else
  echo "mypy not installed, skipping"
fi
