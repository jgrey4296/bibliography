#!/usr/bin/env bash
set -euo pipefail

header "biblio build [-no-clean] --conf {target:main} --out {out:.temp/site} {src}"
if help_flag "$@"; then
    echo -e "Build Sphinx from bibtex files
Uses \$BIBLIO_ROOT
Args:
-no-clean         : don't delete existing site files
--conf {conf dir} : the dir for the conf.py
--out  {out dir}  : the subdir of .temp/site to build into
{src dir}         : the dir of source .rst and .bib files

"
    exit 0
fi
