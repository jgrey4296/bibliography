#!/usr/bin/env bash
set -euo pipefail


header "TODO biblio post"
uv run --script "$BIBLIO_SRC/scripts/media_post.py" "$@"
exit 1
