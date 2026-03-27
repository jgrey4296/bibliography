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
usage: polyglot task stub [args ...] [-h]

positional arguments:
args          :

options:
-h, --help      : show this help message and exit
--window {int}  :
--collect       :

"

maybe-print-help "leaf" 0 "$HELP_TEXT" "$@"
