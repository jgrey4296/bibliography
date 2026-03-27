#!/usr/bin/env bash
# 1.check.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail


function check-environment () {
    subhead "Checking Environment"
    has_failed=0

    if [[ -z "${POLYGLOT_ROOT:-}" ]]; then
        has_failed=1
        echo -e "!-- No POLYGLOT_ROOT has been defined"
    fi

    if [[ "$has_failed" -gt 0 ]]; then
        fail "Missing EnvVars"
    fi
}

check-environment
