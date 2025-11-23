#!/usr/bin/env bash
set -o nounset
set -o pipefail

source "$POLY_SRC/lib/lib-util.bash"

is-help-flag "${@: -1}"
case "$?" in
    1)
        echo "Task: bookmarks

Extract bookmarks from firefox into the total.bookmarks file.
"
        exit 2
    ;;
    *) ;;
esac
