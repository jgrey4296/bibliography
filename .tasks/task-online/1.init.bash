#!/usr/bin/env bash
set -euo pipefail

header "biblio online"
uv run --script "$BIBLIO_SRC/scripts/bib_online.py" "$@"
