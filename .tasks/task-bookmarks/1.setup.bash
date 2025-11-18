#!/usr/bin/env bash
set -euo pipefail

header "biblio bookmarks"
uv run --script "$BIBLIO_SRC/scripts/bookmarks.py" "$@"
