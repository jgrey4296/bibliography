#!/usr/bin/env bash
# 1.check.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

function check-environment () {
    subhead "Checking Environment"
    has_failed=0

    if [[ -z "${POLYGLOT_TEMP:-}" ]]; then
        has_failed=1
        echo -e "!-- No POLYGLOT_TEMP has been defined"
    fi
    if [[ -z "${BIBLIO_TEMPLATE_DIR:-}" ]]; then
        has_failed=1
        echo -e "!-- No BIBLIO_TEMPLATE_DIR has been defined"
    fi

    if [[ "$has_failed" -gt 0 ]]; then
        fail "Missing EnvVars"
    fi
}

check-environment
