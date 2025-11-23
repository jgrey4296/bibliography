#!/usr/bin/env bash
set -o nounset
set -o pipefail

source "$POLY_SRC/lib/lib-util.bash"

is-help-flag "${@: -1}"
case "$?" in
    1)
        echo "Task: chunk

Split large bibtex files into smaller ones.
"
        exit 2
    ;;
    *) ;;
esac
