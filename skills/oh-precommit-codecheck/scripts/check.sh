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

# check.sh — Unified code check entry point
# Usage: check.sh [--json] <file1> [file2] ...
#
# Dispatches files to appropriate checkers by extension:
#   .cpp/.h/.c   → CodeArts Check (codecheck-ide-engine + huawei clang-tidy)
#   .py          → pylint + flake8
#   .sh          → shellcheck + bashate-mod-ds
#   .gn/.gni     → gn format --dry-run
#   all above    → copyright header check

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve tools dir: prefer ~/.codecheck-tools, fallback to /tmp/codecheck-engine (legacy)
if [[ -f "${HOME}/.codecheck-tools/codecheck-ide-engine.jar" ]]; then
    TOOLS_DIR="${HOME}/.codecheck-tools"
elif [[ -f "/tmp/codecheck-engine/codecheck-ide-engine.jar" ]]; then
    TOOLS_DIR="/tmp/codecheck-engine"
else
    TOOLS_DIR="${HOME}/.codecheck-tools"
fi

# Temp file to collect defects (avoids subshell variable loss)
DEFECT_TMP=$(mktemp /tmp/codecheck-defects-XXXXXX.txt)
trap 'rm -f "${DEFECT_TMP}"' EXIT

# ── Parse arguments ──────────────────────────────────────────────────
JSON_OUTPUT=false
FILES=()
for arg in "$@"; do
    if [[ "${arg}" == "--json" ]]; then
        JSON_OUTPUT=true
    else
        FILES+=("${arg}")
    fi
done

if [[ ${#FILES[@]} -eq 0 ]]; then
    echo "Usage: check.sh [--json] <file1> [file2] ..."
    exit 1
fi

# ── Run setup (ensure tools are available) ───────────────────────────
bash "${SCRIPT_DIR}/setup.sh" 2>&1 | grep -E "^\[setup\] (WARNING|Done)" || true

# ── Classify files by type ───────────────────────────────────────────
CPP_FILES=()
PY_FILES=()
SH_FILES=()
GN_FILES=()
ALL_CHECKABLE_FILES=()
SKIPPED_FILES=()

for f in "${FILES[@]}"; do
    if [[ ! -f "${f}" ]]; then
        SKIPPED_FILES+=("${f} (not found)")
        continue
    fi
    real_f=$(realpath "${f}")
    case "${f}" in
        *.cpp|*.h|*.c|*.cc|*.cxx|*.hpp)
            CPP_FILES+=("${real_f}")
            ALL_CHECKABLE_FILES+=("${real_f}")
            ;;
        *.py)
            PY_FILES+=("${real_f}")
            ALL_CHECKABLE_FILES+=("${real_f}")
            ;;
        *.sh)
            SH_FILES+=("${real_f}")
            ALL_CHECKABLE_FILES+=("${real_f}")
            ;;
        *.gn|*.gni)
            GN_FILES+=("${real_f}")
            ALL_CHECKABLE_FILES+=("${real_f}")
            ;;
        *)
            SKIPPED_FILES+=("${f} (unsupported type)")
            ;;
    esac
done

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 0. Copyright — all file types
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if [[ ${#ALL_CHECKABLE_FILES[@]} -gt 0 ]]; then
    echo "[copyright] Checking ${#ALL_CHECKABLE_FILES[@]} file(s)..."
    bash "${SCRIPT_DIR}/check_copyright.sh" "${DEFECT_TMP}" "${ALL_CHECKABLE_FILES[@]}"
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. C/C++ — CodeArts Check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if [[ ${#CPP_FILES[@]} -gt 0 ]]; then
    ENGINE_JAR="${TOOLS_DIR}/codecheck-ide-engine.jar"
    if [[ ! -f "${ENGINE_JAR}" ]]; then
        echo "[cpp] SKIP: CodeArts engine not installed. Run setup.sh first."
    else
        echo "[cpp] Checking ${#CPP_FILES[@]} C/C++ file(s)..."

        PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

        OUTPUT_DIR=$(mktemp -d /tmp/codecheck-output-XXXXXX)
        CONFIG_DIR="${OUTPUT_DIR}/checkPath"
        mkdir -p "${CONFIG_DIR}"

        # Build sourceFiles JSON array
        SOURCE_JSON="["
        FIRST=true
        for f in "${CPP_FILES[@]}"; do
            if [[ "${FIRST}" == true ]]; then
                FIRST=false
            else
                SOURCE_JSON+=","
            fi
            SOURCE_JSON+="\"${f}\""
        done
        SOURCE_JSON+="]"

        cat > "${CONFIG_DIR}/source.txt" <<EOJSON
{"projectRoot": "${PROJECT_ROOT}", "sourceFiles": ${SOURCE_JSON}, "sourceDirs": [], "exclude": ""}
EOJSON

        # Check for compile_commands.json
        COMPILE_DB=""
        for candidate in \
            "${PROJECT_ROOT}/build/compile_commands.json" \
            "${PROJECT_ROOT}/compile_commands.json"; do
            if [[ -f "${candidate}" ]]; then
                COMPILE_DB="${candidate}"
                break
            fi
        done
        if [[ -z "${COMPILE_DB}" ]]; then
            COMPILE_DB=$(find "${PROJECT_ROOT}/out" -maxdepth 2 -name "compile_commands.json" 2>/dev/null | head -1)
        fi

        if [[ -n "${COMPILE_DB}" ]]; then
            cat > "${CONFIG_DIR}/extraParam.json" <<EOJSON2
{"compileCommandsJsonDir": "$(dirname "${COMPILE_DB}")"}
EOJSON2
            echo "[cpp] Using compile_commands.json: ${COMPILE_DB}"
        fi

        java -jar "${ENGINE_JAR}" \
            --report-output-dir "${OUTPUT_DIR}" \
            --check-config-file "${CONFIG_DIR}/source.txt" \
            --lang "zh-cn" --mode "local" \
            > "${OUTPUT_DIR}/engine.log" 2>&1 || true

        DEFECTS_FILE="${OUTPUT_DIR}/defects.json"
        if [[ -f "${DEFECTS_FILE}" ]]; then
            # Build allowed-files list for filtering
            ALLOWED_FILES_ARG=""
            for af in "${CPP_FILES[@]}"; do
                ALLOWED_FILES_ARG+="${af},"
            done
            python3 -c "
import json, sys
try:
    allowed = set(sys.argv[2].rstrip(',').split(','))
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    defects = data if isinstance(data, list) else data.get('defects', data.get('Defects', []))
    for d in defects:
        filepath = d.get('buggyFilePath', d.get('filePath', ''))
        if filepath not in allowed:
            continue
        line = d.get('startRowNumber', d.get('buggyLine', d.get('line', '?')))
        rule = d.get('defectType', d.get('checkerName', 'unknown'))
        msg = d.get('description', d.get('message', '')).replace('|', ' ')
        criterion = d.get('criterionName', '')
        if criterion:
            msg = criterion + ' -- ' + msg
        print(f'codearts|{filepath}|{line}|{rule}|{msg}')
except Exception as e:
    print(f'codearts|ERROR|0|parse-error|Failed to parse defects.json: {e}', file=sys.stderr)
" "${DEFECTS_FILE}" "${ALLOWED_FILES_ARG}" >> "${DEFECT_TMP}" 2>/dev/null
        fi

        rm -rf "${OUTPUT_DIR}"
    fi
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. Python — pylint + flake8
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if [[ ${#PY_FILES[@]} -gt 0 ]]; then
    echo "[py] Checking ${#PY_FILES[@]} Python file(s)..."
    bash "${SCRIPT_DIR}/check_python.sh" "${DEFECT_TMP}" "${PY_FILES[@]}"
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Shell — shellcheck + bashate-mod-ds
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if [[ ${#SH_FILES[@]} -gt 0 ]]; then
    echo "[sh] Checking ${#SH_FILES[@]} Shell file(s)..."
    bash "${SCRIPT_DIR}/check_shell.sh" "${DEFECT_TMP}" "${SH_FILES[@]}"
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. GN — gn format --dry-run
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if [[ ${#GN_FILES[@]} -gt 0 ]]; then
    if command -v gn &>/dev/null; then
        echo "[gn] Checking ${#GN_FILES[@]} GN file(s)..."
        for f in "${GN_FILES[@]}"; do
            gn format --dry-run "${f}" >/dev/null 2>&1
            GN_EXIT=$?
            if [[ ${GN_EXIT} -eq 2 ]]; then
                echo "gn|${f}|1|gn-format|File needs formatting (run: gn format ${f})" >> "${DEFECT_TMP}"
            elif [[ ${GN_EXIT} -eq 1 ]]; then
                echo "gn|${f}|1|gn-parse-error|GN parse error" >> "${DEFECT_TMP}"
            fi
        done
    else
        echo "[gn] SKIP: gn not installed"
    fi
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Output results
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL_DEFECTS=0
if [[ -f "${DEFECT_TMP}" ]]; then
    TOTAL_DEFECTS=$(wc -l < "${DEFECT_TMP}" | tr -d ' ')
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo " Code Check Results"
echo "═══════════════════════════════════════════════════════════════"

for s in "${SKIPPED_FILES[@]+"${SKIPPED_FILES[@]}"}"; do
    echo " SKIP: ${s}"
done

if [[ ${TOTAL_DEFECTS} -eq 0 ]]; then
    CHECKED=$((${#CPP_FILES[@]} + ${#PY_FILES[@]} + ${#SH_FILES[@]} + ${#GN_FILES[@]}))
    echo " All ${CHECKED} file(s) passed - 0 defects found."
    echo "═══════════════════════════════════════════════════════════════"

    if [[ "${JSON_OUTPUT}" == true ]]; then
        echo '{"total_defects": 0, "defects": []}'
    fi
    exit 0
fi

echo " Found ${TOTAL_DEFECTS} defect(s):"
echo "-------------------------------------------------------------------"

if [[ "${JSON_OUTPUT}" == true ]]; then
    echo -n '{"total_defects": '"${TOTAL_DEFECTS}"', "defects": ['
    FIRST=true
    while IFS='|' read -r tool file line rule msg; do
        if [[ "${FIRST}" == true ]]; then
            FIRST=false
        else
            echo -n ","
        fi
        msg=$(echo "${msg}" | sed 's/"/\\"/g')
        file=$(echo "${file}" | sed 's/"/\\"/g')
        echo -n "{\"file\":\"${file}\",\"line\":${line:-0},\"rule\":\"${rule}\",\"message\":\"${msg}\",\"tool\":\"${tool}\"}"
    done < "${DEFECT_TMP}"
    echo ']}'
else
    printf " %-10s %-50s %-6s %s\n" "TOOL" "FILE" "LINE" "RULE / MESSAGE"
    echo "-------------------------------------------------------------------"
    GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
    while IFS='|' read -r tool file line rule msg; do
        if [[ -n "${GIT_ROOT}" ]]; then
            short_file="${file#"${GIT_ROOT}"/}"
        else
            short_file="${file}"
        fi
        printf " %-10s %-50s %-6s %s\n" "[${tool}]" "${short_file}" "${line}" "${rule}: ${msg}"
    done < "${DEFECT_TMP}"
fi

echo "═══════════════════════════════════════════════════════════════"
exit 1
