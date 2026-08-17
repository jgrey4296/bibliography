#!/usr/bin/env bash
# init-asdf.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

[[ -n "${GITHUB_ENV:-}" ]] || { echo "Not in a Github Environment"; exit 0; }

echo "- Initialising for Github Actions"

ASDF_PLUGIN_LIST=".asdf.plugins"

# asdf plugin add
if [[ -e "${ASDF_PLUGIN_LIST:-}" ]]; then
    echo "- Adding ASDF plugins"
    while read -r pname url; do
        if [[ -n "$pname" ]]; then
            asdf plugin add "${pname}" "${url}" 2>/dev/null
        fi
    done < "$ASDF_PLUGIN_LIST"
fi

echo "- Installing asdf tools"
asdf install
asdf reshim

echo "- Updating env"
direnv allow
direnv export gha > "${GITHUB_ENV}"

echo "- Installing python venv: ${UV_PROJECT_ENVIRONMENT:-}"
uv venv >/dev/null 2>/dev/null
uv sync >/dev/null 2>/dev/null

echo "- Initialisation complete"
