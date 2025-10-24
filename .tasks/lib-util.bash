#!/usr/bin/env bash
# Utilities for polyglot

function debug () {
    if [ "${VERBOSE:-0}" -eq 1 ]; then
        echo "$@"
    fi
}

function fail () {
    echo "Failed: $*"
    exit 1
}

function header () {
    echo "-------------------------"
    echo "* $1"
    echo "-------------------------"
}

function subhead () {
    echo "---------- $1"
}

function tdot () {
    echo "... $1"
}

function sep () {
    echo "-------------------------"
}

function get_activated () {
    # Get all activated subprojects
    fdfind --base-directory "${POLYGLOT_ROOT}" --hidden "\.active" "./src" --exec dirname

}

function help_flag () {
    case "${1:-}" in
        -h|--help) return 0 ;;
        *) return 1 ;;
    esac
}
