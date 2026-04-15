#!/usr/bin/env bash
# init-asdf.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

[[ -n "${GITHUB_ENV:-}" ]] || { echo "Not in a Github Environment"; exit 0; }

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

asdf install
asdf reshim

direnv allow
echo "- Updating Github Environment"
direnv export gha >> "$GITHUB_ENV"
