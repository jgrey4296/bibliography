#!/usr/bin/env bash
set -euo pipefail

# todo: have a file of backup targets?
header "biblio --backup"
if help_flag "$@"; then
    echo "
Backup arg 1 to arg 2 using rsync
Uses BIBLIO_LIB
"
    exit 0
fi

source="${1:-$BIBLIO_LIB}"
target="${2:-/media/john/solid_ext4/library}"
header "Biblio Library Backup: $source -> $target"
rsync --archive --progress "$source" "$target"
