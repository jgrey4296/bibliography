#!/usr/bin/env bash
# place in $root/.tasks/task-{name}/0.help.bash
# and chmod +x it.
set -o nounset
set -o pipefail

# shellcheck disable=SC1091
source "$POLY_SRC/lib/lib-util.bash"
[[ -e "$POLYGLOT_ROOT/.tasks/task-util.bash" ]] && source "$POLYGLOT_ROOT/.tasks/task-util.bash"


HELP_TEXT="
usage: polyglot task report [args ...] [-h]

Create a report.rst for the project.

positional arguments:
args          :

options:
-h, --help    : show this help message and exit
--collect
--out

"

maybe-print-help "leaf" 0 "$HELP_TEXT" "$@"
