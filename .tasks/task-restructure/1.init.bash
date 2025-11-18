#!/usr/bin/env bash
set -euo pipefail

header "biblio move"
uv run --script "$BIBLIO_SRC/scripts/lib_restructure.py" "$@"
