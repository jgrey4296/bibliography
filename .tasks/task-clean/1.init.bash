#!/usr/bin/env bash
set -euo pipefail

echo "cleanup"
uv run --script "$BIBLIO_SRC/scripts/clean_todos.py" "$@"
