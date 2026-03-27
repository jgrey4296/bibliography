#!/usr/bin/env bash
# 1.check.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

function check-environment () {
    subhead "Checking Environment"
    has_failed=0

    if [[ -z "${BIBLIO_TODO:-}" ]]; then
        has_failed=1
        echo -e "!-- No BIBLIO_TODO has been defined"
    fi

    if [[ "$has_failed" -gt 0 ]]; then
        fail "Missing EnvVars"
    fi
}

check-environment
