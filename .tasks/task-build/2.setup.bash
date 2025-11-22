#!/usr/bin/env bash
set -euo pipefail


do_clean=1
conf="$BIBLIO_ROOT"
src="$conf/"
out="$BIBLIO_ROOT/.temp"
site_out="$out/site"
while [[ $# -gt 0 ]]; do
    case $1 in
        -no-clean|--no-clean)
            do_clean=0
            ;;
        --conf)
            shift
            echo "Conf: $1"
            conf=$(realpath "$1")
            ;;
        --out)
            shift
            echo "Out: $1"
            site_out=$(realpath "$site_out/$1")
            ;;
        *) # Positional
            echo "Src: $1"
            src=$(realpath "$1")
            ;;
    esac
    shift
done
