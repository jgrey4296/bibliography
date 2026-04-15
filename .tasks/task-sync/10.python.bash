#!/usr/bin/env bash
# 10.python.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

uv sync --all-groups --all-extras
