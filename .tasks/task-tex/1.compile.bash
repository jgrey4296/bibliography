#!/usr/bin/env bash
set -euo pipefail

source "$POLY_SRC/lib/lib-util.bash"

output="$POLYGLOT_ROOT/.temp/tex"
template_dir="$POLYGLOT_ROOT/templates_"
# collect tex files, generate separate chapters for each,
# and export the bibtex files with latex encoding
uv script --run "$BIBLIO_SRC/scripts/prepare_tex.py" \
    --template-dir "$template_dir" \
    "$@"

exit 1
# compile each chapter
lualatex --interaction=nonstopmode --output-directory="$output" "$output"/*.tex > /dev/null
BIBINPUT="$output:${BIBINPUTS:-}" bibtex --terse "$output"/*.tex > /dev/null
lualatex --interaction=nonstopmode --output-directory="$output" "$output"/*.tex /dev/null
lualatex --interaction=nonstopmode --output-directory="$output" "$output"/*.tex /dev/null

# join them together
pdftk cat "$output"/*.pdf output "$output/library.pdf"
