#!/usr/bin/env bash
set -euo pipefail

header "biblio stubs"
uv run --script "$BIBLIO_SRC/scripts/make_stubs.py" "$@"
