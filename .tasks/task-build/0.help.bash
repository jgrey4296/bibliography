#!/usr/bin/env bash
set -o nounset
set -o pipefail

source "$POLY_SRC/lib/lib-util.bash"

is-help-flag "${@: -1}"
case "$?" in
    1)
        echo -e "Build Sphinx from bibtex files
Uses \$POLYGLOT_ROOT
Args:
-nc | -no-clean   : don't delete existing site files
--conf {conf dir} : the dir for the conf.py
--out  {out dir}  : the subdir of .temp/site to build into
{src dir}         : the dir of source .rst and .bib files

"
        exit 2
    ;;
    *) ;;
esac
