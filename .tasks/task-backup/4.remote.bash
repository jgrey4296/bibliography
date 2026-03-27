#!/usr/bin/env bash
# 3.remote.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

# shellcheck disable=SC1091
source "$POLY_SRC/lib/lib-util.bash"
if [[ -e "$POLYGLOT_ROOT/.tasks/task-util.bash" ]]; then
   # shellcheck disable=SC1091
    source "$POLYGLOT_ROOT/.tasks/task-util.bash"
fi

subhead "Backup up to remote"

source="${1:-$BIBLIO_LIB}"
target="john@192.168.1.216:/media/users/documents_bkup/library"

subhead "Source: $source"
echo "->"
subhead "Target: $target"

([[ -n "$source" ]] && [[ -n "$target" ]]) || exit 1

rsync --archive --progress "$source" "$target"
