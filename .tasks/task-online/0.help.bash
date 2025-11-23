#!/usr/bin/env bash
set -o nounset
set -o pipefail

source "$POLY_SRC/lib/lib-util.bash"

is-help-flag "${@: -1}"
case "$?" in
    1)
        echo "Task: Online
TODO

Download new online urls as pdfs.
"
        exit 2
    ;;
    *) ;;
esac
