#!/usr/bin/env bash
# 1.check.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

# shellcheck disable=SC1091
[[ -e "$POLY_SRC/lib/lib.bash" ]] && source "$POLY_SRC/lib/lib.bash"
# shellcheck disable=SC1091
[[ -e "$(poly-dir)/task-util.bash" ]] && source "$(poly-dir)/task-util.bash"

function check-environment () {
    subhead "Checking Environment"
    has_failed=()

    if [[ -z "${POLYGLOT_ROOT:-}" ]]; then
        has_failed+=("POLYGLOT_ROOT")
    fi

    [[ -z "${has_failed[@]:-}" ]] || fail "Missing EnvVars: ${has_failed[*]}"
}

check-environment
