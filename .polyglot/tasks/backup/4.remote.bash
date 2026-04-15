#!/usr/bin/env bash
# 3.remote.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

# shellcheck disable=SC1091
[[ -e "$POLY_SRC/lib/lib.bash" ]] && source "$POLY_SRC/lib/lib.bash"
# shellcheck disable=SC1091
[[ -e "$(poly-dir)/task-util.bash" ]] && source "$(poly-dir)/task-util.bash"

subhead "Backup up to remote"

source="${1:-$BIBLIO_LIB}"
target="john@192.168.1.216:/media/users/documents_bkup/library"

subhead "Source: $source"
echo "->"
subhead "Target: $target"

([[ -n "$source" ]] && [[ -n "$target" ]]) || exit 1

rsync --archive --progress "$source" "$target"
