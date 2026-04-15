#!/usr/bin/env bash
# test-hook2.sh -*- mode: sh -*-
# exit on various failures:

while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--target)
            echo "Target: $2"
            ;;
        --*=*)
            echo "Assignment: $1"
            ;;
        *) # Positional
            echo "Positional: $1"
            ;;
    esac
    shift
done

echo "Basic Local Shell Hook: $@"
exit 0
