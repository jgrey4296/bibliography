#!/usr/bin/env bash
set -euo pipefail

uv run sphinx-build \
    --conf-dir "$conf" \
    --doctree-dir "$out/doctrees" \
    --warning-file "$conf/.temp/logs/sphinx.log" \
    --builder "bibhtml" \
    "$src" "$site_out"
