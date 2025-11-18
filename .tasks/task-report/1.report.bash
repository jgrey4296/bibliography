#!/usr/bin/env bash
set -euo pipefail

header "biblio report"
uv run --script "$BIBLIO_SRC/scripts/bib_report.py" "$@"
