#!/usr/bin/env bash
set -o nounset
set -o pipefail

source "$POLY_SRC/lib/lib-util.bash"

is-help-flag "${@: -1}"
case "$?" in
    1)
        echo "Task: report

Generate an .rst report on the bibtex files.
"
        exit "$PRINTED_HELP"
    ;;
    *) ;;
esac
