#!/usr/bin/env bash
# make-django.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

uv run django-admin startproject dynamic_ "${POLYGLOT_ROOT}"
uv run manage.py startpp polls ./dynamic_/polls

echo "## ---- For Django:\n\n## ----" >> "${POLYGLOT_ROOT}/.envrc"
