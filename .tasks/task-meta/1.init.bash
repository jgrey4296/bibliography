#!/usr/bin/env bash
set -euo pipefail

header "biblio metadata"
uv run --script "$BIBLIO_SRC/scripts/apply_metadata.py" "$@"
