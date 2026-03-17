#!/usr/bin/env bash
# Copyright (c) 2025-2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# check_shell.sh — Shell linter checks (shellcheck + bashate-mod-ds)
# Usage: check_shell.sh <output_file> <file1.sh> [file2.sh] ...
#
# Appends defects to <output_file> in format: tool|file|line|rule|message
# Rules match the gate CI exactly.

set -uo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: check_shell.sh <output_file> <file1.sh> [file2.sh] ..."
    exit 1
fi

DEFECT_TMP="$1"
shift

# Gate-identical shellcheck rules (include only these)
SHELLCHECK_RULES="SC1068,SC1106,SC1133,SC2002,SC2003,SC2006,SC2010,SC2024,SC2034,SC2041,SC2045,SC2064,SC2066,SC2067,SC2081,SC2086,SC2088,SC2093,SC2115,SC2142,SC2144,SC2148,SC2152,SC2164,SC2166,SC2172,SC2173,SC2222,SC2253"

# Gate-identical bashate rules (ignore these, check everything else)
BASHATE_IGNORE="E006,E042"

HAS_SHELLCHECK=false
HAS_BASHATE=false
command -v shellcheck &>/dev/null && HAS_SHELLCHECK=true
command -v bashate-mod-ds &>/dev/null && HAS_BASHATE=true

if [[ "${HAS_SHELLCHECK}" == false ]]; then
    echo "[sh] SKIP shellcheck: not installed (apt install shellcheck)"
fi
if [[ "${HAS_BASHATE}" == false ]]; then
    echo "[sh] SKIP bashate-mod-ds: not installed (pip install bashate-mod-ds)"
fi

for f in "$@"; do
    if [[ ! -f "${f}" ]]; then
        echo "[sh] SKIP: ${f} (not found)"
        continue
    fi

    if [[ "${HAS_SHELLCHECK}" == true ]]; then
        shellcheck -f gcc -i "${SHELLCHECK_RULES}" "${f}" 2>/dev/null | while IFS= read -r line; do
            if [[ "${line}" =~ ^(.+):([0-9]+):[0-9]+:\ (.+)$ ]]; then
                pfile="${BASH_REMATCH[1]}"
                pline="${BASH_REMATCH[2]}"
                pmsg="${BASH_REMATCH[3]}"
                prule=$(echo "${pmsg}" | grep -oP 'SC[0-9]{4}' | head -1)
                pmsg_clean=$(echo "${pmsg}" | sed 's/|/ /g')
                echo "shellcheck|${pfile}|${pline}|${prule:-shellcheck}|${pmsg_clean}" >> "${DEFECT_TMP}"
            fi
        done
    fi

    if [[ "${HAS_BASHATE}" == true ]]; then
        bashate-mod-ds -i "${BASHATE_IGNORE}" "${f}" 2>/dev/null | while IFS= read -r line; do
            if [[ "${line}" =~ ^(.+):([0-9]+):[0-9]+:\ (.+)$ ]]; then
                pfile="${BASH_REMATCH[1]}"
                pline="${BASH_REMATCH[2]}"
                pmsg="${BASH_REMATCH[3]}"
                prule=$(echo "${pmsg}" | grep -oP 'E[0-9]{3}' | head -1)
                pmsg_clean=$(echo "${pmsg}" | sed 's/|/ /g')
                echo "bashate|${pfile}|${pline}|${prule:-bashate}|${pmsg_clean}" >> "${DEFECT_TMP}"
            fi
        done
    fi
done
