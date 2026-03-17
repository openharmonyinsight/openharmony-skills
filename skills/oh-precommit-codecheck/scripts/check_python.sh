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

# check_python.sh — Python linter checks (pylint + flake8)
# Usage: check_python.sh <output_file> <file1.py> [file2.py] ...
#
# Appends defects to <output_file> in format: tool|file|line|rule|message
# Rules match the gate CI exactly.

set -uo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: check_python.sh <output_file> <file1.py> [file2.py] ..."
    exit 1
fi

DEFECT_TMP="$1"
shift

# Gate-identical pylint rules
PYLINT_RULES="C0121,C0123,C0304,C0305,C0321,C0410,C0411,C1801,E0303,E0304,E0701,E1111,R1708,R1710,W0101,W0102,W0109,W0123,W0150,W0201,W0212,W0221,W0231,W0601,W0706,W0640,W1201,W3101"

# Gate-identical flake8 rules
FLAKE8_RULES="C101,EXE002,S506,S602,N801,N802,N803,N805,N806,N807,N815,N816,N817"

HAS_PYLINT=false
HAS_FLAKE8=false
command -v pylint &>/dev/null && HAS_PYLINT=true
command -v flake8 &>/dev/null && HAS_FLAKE8=true

if [[ "${HAS_PYLINT}" == false ]]; then
    echo "[py] SKIP pylint: not installed (pip install pylint)"
fi
if [[ "${HAS_FLAKE8}" == false ]]; then
    echo "[py] SKIP flake8: not installed (pip install flake8 flake8-coding flake8-builtins pep8-naming flake8-executable flake8-bandit)"
fi

for f in "$@"; do
    if [[ ! -f "${f}" ]]; then
        echo "[py] SKIP: ${f} (not found)"
        continue
    fi

    if [[ "${HAS_PYLINT}" == true ]]; then
        pylint -s false \
            --timeout-methods "subprocess.Popen.communicate" \
            --disable=all \
            -e "${PYLINT_RULES}" \
            "${f}" 2>/dev/null | while IFS= read -r line; do
                if [[ "${line}" =~ ^(.+):([0-9]+):[0-9]+:\ (.+)$ ]]; then
                    pfile="${BASH_REMATCH[1]}"
                    pline="${BASH_REMATCH[2]}"
                    pmsg="${BASH_REMATCH[3]}"
                    prule=$(echo "${pmsg}" | grep -oP '[A-Z][0-9]{4}' | head -1)
                    pmsg_clean=$(echo "${pmsg}" | sed 's/|/ /g')
                    echo "pylint|${pfile}|${pline}|${prule:-pylint}|${pmsg_clean}" >> "${DEFECT_TMP}"
                fi
            done
    fi

    if [[ "${HAS_FLAKE8}" == true ]]; then
        flake8 --select "${FLAKE8_RULES}" "${f}" 2>/dev/null | while IFS= read -r line; do
            if [[ "${line}" =~ ^(.+):([0-9]+):[0-9]+:\ (.+)$ ]]; then
                pfile="${BASH_REMATCH[1]}"
                pline="${BASH_REMATCH[2]}"
                pmsg="${BASH_REMATCH[3]}"
                prule=$(echo "${pmsg}" | grep -oP '[A-Z][0-9]{2,4}' | head -1)
                pmsg_clean=$(echo "${pmsg}" | sed 's/|/ /g')
                echo "flake8|${pfile}|${pline}|${prule:-flake8}|${pmsg_clean}" >> "${DEFECT_TMP}"
            fi
        done
    fi
done
