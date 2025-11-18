#!/usr/bin/env bash
set -euo pipefail

echo -e "Building:\n- (conf:$conf)\n- (src:$src)\n->(out:$site_out)"
if [[ "$do_clean" -gt 0 ]] && [[ -d "${site_out}" ]]; then
    rm -r "${site_out}"
fi
