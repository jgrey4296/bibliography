#!/usr/bin/env bash
# place in $root/.tasks/task-{name}/0.help.bash
# and chmod +x it.
set -o nounset
set -o pipefail

# shellcheck disable=SC1091
source "$POLY_SRC/lib/lib-util.bash"
if [[ -e "$POLYGLOT_ROOT/.tasks/task-util.bash" ]]; then
    source "$POLYGLOT_ROOT/.tasks/task-util.bash"
fi

HELP_TEXT="
usage: polyglot task chunk [args ...] [-h]

Chunk larger bibtex files into smaller ones.

positional arguments:
args          :

options:
-h, --help    : show this help message and exit
--size {int}  :
--collect     :
--failures    :

"


maybe-print-help "leaf" 0 "$HELP_TEXT" "$@"
