#!/usr/bin/env bash
set -euo pipefail

header "biblio chunk"
uv run --script "$BIBLIO_SRC/scripts/bib_chunk.py" "$@"
