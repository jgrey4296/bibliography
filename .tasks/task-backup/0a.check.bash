#!/usr/bin/env bash
# 0a.check.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

source "$POLY_SRC/lib/lib-util.bash"

has_failed=0
if [[ -z "${BIBLIO_LIB:-}" ]]; then
    has_failed=1
    echo -e "!-- No BIBLIO_LIB has been defined"
fi

if [[ -z "${BIBLIO_BKUP:-}" ]]; then
    has_failed=1
    echo -e "!-- No BIBLIO_BKUP has been defined"
fi

if [[ "$has_failed" -gt 0 ]]; then
    fail "Missing EnvVars"
fi
