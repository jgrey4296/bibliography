#!/usr/bin/env bash
set -euo pipefail

header "biblio format"
uv run --script "$BIBLIO_SRC/scripts/bib_format.py" "$@"
