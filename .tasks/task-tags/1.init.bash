#!/usr/bin/env bash
set -euo pipefail

header "biblio tags"
uv run --script "$BIBLIO_SRC/scripts/update_tags.py" "$@"
