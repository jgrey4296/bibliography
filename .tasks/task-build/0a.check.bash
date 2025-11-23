#!/usr/bin/env bash
# 0a.check.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

source "$POLY_SRC/lib/lib-util.bash"

# Basic envvar check logic:
has_failed=0
if [[ -z "${POLYGLOT_ROOT:-}" ]]; then
    has_failed=1
    echo -e "!-- No POLYGLOT_ROOT has been defined"
fi

if [[ "$has_failed" -gt 0 ]]; then
    fail "Missing EnvVars"
fi
