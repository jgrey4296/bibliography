#!/usr/bin/env bash
# 1.check.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

function check-environment () {
    subhead "Checking Environment"
    has_failed=0

    if [[ "$has_failed" -gt 0 ]]; then
        fail "Missing EnvVars"
    fi
}

check-environment
