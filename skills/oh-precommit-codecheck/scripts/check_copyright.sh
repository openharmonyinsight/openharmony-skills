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

# check_copyright.sh — Copyright header checks
# Usage: check_copyright.sh <output_file> <file1> [file2] ...
#
# Appends defects to <output_file> in format: tool|file|line|rule|message
# Checks:
#   1. File has "Copyright (c)" header
#   2. Copyright year includes current year (e.g., 2024-2026 or 2026)
#   3. For .cpp/.c/.h/.hpp/.groovy files: first line must start with "/**"

set -uo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: check_copyright.sh <output_file> <file1> [file2] ..."
    exit 1
fi

DEFECT_TMP="$1"
shift

CUR_YEAR=$(date +%Y)

# File extensions that require copyright checks
COPYRIGHT_EXTS='\.cpp$|\.c$|\.hpp$|\.h$|\.js$|\.ts$|\.ets$|\.py$|\.sh$|\.groovy$|\.Jenkinsfile$|\.gn$|\.gni$'

# File extensions that require "/**" as first line (C-style block comment)
BLOCK_COMMENT_EXTS='\.cpp$|\.c$|\.hpp$|\.h$|\.groovy$|\.Jenkinsfile$'

for f in "$@"; do
    if [[ ! -f "${f}" ]]; then
        echo "[copyright] SKIP: ${f} (not found)"
        continue
    fi

    # Only check files with known extensions
    if ! echo "${f}" | grep -qE "${COPYRIGHT_EXTS}"; then
        continue
    fi

    real_f=$(realpath "${f}")

    # Check 1: Has copyright header at all
    if ! grep -iq 'Copyright (c) ' "${real_f}"; then
        echo "copyright|${real_f}|1|no-copyright|Missing copyright header" >> "${DEFECT_TMP}"
        continue
    fi

    # Check 2: Copyright year includes current year
    if ! grep -Eiq "Copyright \(c\).*([0-9]{4}-)?${CUR_YEAR} " "${real_f}"; then
        echo "copyright|${real_f}|1|wrong-year|Copyright year does not include ${CUR_YEAR}" >> "${DEFECT_TMP}"
    fi

    # Check 3: C/C++/groovy files must start with "/**"
    if echo "${f}" | grep -qE "${BLOCK_COMMENT_EXTS}"; then
        first_line=$(head -n 1 "${real_f}")
        if [[ "${first_line}" != "/**" ]]; then
            echo "copyright|${real_f}|1|wrong-comment-style|First line must be '/**' (block comment), got '${first_line}'" >> "${DEFECT_TMP}"
        fi
    fi
done
