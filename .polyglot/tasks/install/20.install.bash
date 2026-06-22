#!/usr/bin/env bash
# 20.install.bash -*- mode: sh -*-
#set -o errexit
set -o nounset
set -o pipefail

# shellcheck disable=SC1091
[[ -e "$POLY_SRC/lib/lib.bash" ]] && source "$POLY_SRC/lib/lib.bash"
# shellcheck disable=SC1091
[[ -e "$(poly-dir)/task-util.bash" ]] && source "$(poly-dir)/task-util.bash"

echo "Installing into target dir: ${POLYGLOT_INSTALL_DEST} ..."
rsync -v -a "${POLYGLOT_TEMP}/html/" "${POLYGLOT_INSTALL_DEST}"
# install nginx config
# rsync "${POLYGLOT_NGINX_CONF}" "${POLYGLOT_NGINX_DEST}"

# All that remains is so activate by linking to sites-enabled
