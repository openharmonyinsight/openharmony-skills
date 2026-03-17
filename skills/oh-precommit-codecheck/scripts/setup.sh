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

# setup.sh — Ensure codecheck tools are installed
# Checks ~/.codecheck-tools/ first, falls back to /tmp/codecheck-engine/ (legacy)
# Downloads to ~/.codecheck-tools/ if neither exists

set -euo pipefail

TOOLS_DIR="${HOME}/.codecheck-tools"
LEGACY_DIR="/tmp/codecheck-engine"
ENGINE_URL="https://codeheck-chajian-bj4-obs.obs.cn-north-4.myhuaweicloud.com/tool-engines/Linux/codecheck-ide-engine.zip"
CLANGTIDY_URL="https://codeheck-chajian-bj4-obs.obs.cn-north-4.myhuaweicloud.com/tool-engines/lsp-server/Linux/CodeCheckRT.zip"
CURL_TIMEOUT=600

MISSING_TOOLS=()

# ── 1. CodeArts engine ──────────────────────────────────────────────
if [[ -f "${TOOLS_DIR}/codecheck-ide-engine.jar" ]]; then
    echo "[setup] Engine found at ${TOOLS_DIR}"
elif [[ -f "${LEGACY_DIR}/codecheck-ide-engine.jar" ]]; then
    echo "[setup] Engine found at ${LEGACY_DIR} (legacy path)"
    TOOLS_DIR="${LEGACY_DIR}"
else
    echo "[setup] Downloading CodeArts codecheck engine..."
    mkdir -p "${TOOLS_DIR}"
    TMP_ZIP=$(mktemp /tmp/codecheck-engine-XXXXXX.zip)
    if curl -fSL --connect-timeout 10 --max-time "${CURL_TIMEOUT}" --progress-bar \
         -o "${TMP_ZIP}" "${ENGINE_URL}"; then
        TMP_EXTRACT=$(mktemp -d /tmp/codecheck-extract-XXXXXX)
        unzip -qo "${TMP_ZIP}" -d "${TMP_EXTRACT}"
        # zip may contain a top-level directory; find the jar and move contents
        JAR_PATH=$(find "${TMP_EXTRACT}" -name "codecheck-ide-engine.jar" -type f | head -1)
        if [[ -n "${JAR_PATH}" ]]; then
            JAR_DIR=$(dirname "${JAR_PATH}")
            cp -a "${JAR_DIR}"/. "${TOOLS_DIR}"/
        fi
        rm -rf "${TMP_EXTRACT}"
        echo "[setup] Engine installed at ${TOOLS_DIR}"
    else
        echo "[setup] WARNING: Failed to download CodeArts engine (timeout or network error)"
        echo "[setup] C/C++ checks will be skipped"
    fi
    rm -f "${TMP_ZIP}"
fi

# ── 2. Huawei clang-tidy ────────────────────────────────────────────
CLANG_TIDY_BIN="${TOOLS_DIR}/tools/clangtidy/bin/clang-tidy"
if [[ -f "${CLANG_TIDY_BIN}" ]]; then
    echo "[setup] clang-tidy already installed."
elif [[ -f "${LEGACY_DIR}/tools/clangtidy/bin/clang-tidy" ]]; then
    echo "[setup] clang-tidy found at ${LEGACY_DIR} (legacy path)"
else
    echo "[setup] Downloading Huawei clang-tidy..."
    mkdir -p "${TOOLS_DIR}/tools/clangtidy"
    TMP_ZIP=$(mktemp /tmp/codecheck-rt-XXXXXX.zip)
    if curl -fSL --connect-timeout 10 --max-time "${CURL_TIMEOUT}" --progress-bar \
         -o "${TMP_ZIP}" "${CLANGTIDY_URL}"; then
        TMP_EXTRACT=$(mktemp -d /tmp/codecheck-extract-XXXXXX)
        unzip -qo "${TMP_ZIP}" -d "${TMP_EXTRACT}"
        # zip contains CodeCheckRT/ top-level dir with clangtidy/ inside
        TIDY_PATH=$(find "${TMP_EXTRACT}" -name "clang-tidy" -type f -path "*/clangtidy/bin/*" | head -1)
        if [[ -n "${TIDY_PATH}" ]]; then
            # e.g. .../CodeCheckRT/clangtidy/bin/clang-tidy → copy CodeCheckRT/* into tools/clangtidy/
            RT_DIR=$(dirname "${TIDY_PATH}")     # .../clangtidy/bin
            RT_DIR=$(dirname "${RT_DIR}")         # .../clangtidy
            RT_DIR=$(dirname "${RT_DIR}")         # .../CodeCheckRT
            cp -a "${RT_DIR}"/. "${TOOLS_DIR}/tools/clangtidy"/
        fi
        rm -rf "${TMP_EXTRACT}"
        chmod +x "${CLANG_TIDY_BIN}" 2>/dev/null || true
        echo "[setup] clang-tidy installed at ${CLANG_TIDY_BIN}"
    else
        echo "[setup] WARNING: Failed to download Huawei clang-tidy"
    fi
    rm -f "${TMP_ZIP}"
fi

# ── 3. Check Java runtime ───────────────────────────────────────────
if ! command -v java &>/dev/null; then
    MISSING_TOOLS+=("java (required for CodeArts engine)")
fi

# ── 4. Check Python linters ─────────────────────────────────────────
if ! command -v pylint &>/dev/null; then
    MISSING_TOOLS+=("pylint (pip install pylint)")
fi
if ! command -v flake8 &>/dev/null; then
    MISSING_TOOLS+=("flake8 (pip install flake8 flake8-coding flake8-builtins pep8-naming flake8-executable flake8-bandit)")
fi

# ── 5. Check Shell linters ──────────────────────────────────────────
if ! command -v shellcheck &>/dev/null; then
    MISSING_TOOLS+=("shellcheck (apt install shellcheck)")
fi
if ! command -v bashate-mod-ds &>/dev/null; then
    MISSING_TOOLS+=("bashate-mod-ds (pip install bashate-mod-ds)")
fi

# ── 6. Check GN formatter ───────────────────────────────────────────
if ! command -v gn &>/dev/null; then
    MISSING_TOOLS+=("gn (required for BUILD.gn format checking)")
fi

# ── 7. Report missing tools ─────────────────────────────────────────
if [[ ${#MISSING_TOOLS[@]} -gt 0 ]]; then
    echo ""
    echo "[setup] WARNING: The following tools are missing:"
    for tool in "${MISSING_TOOLS[@]}"; do
        echo "  - ${tool}"
    done
    echo ""
    echo "[setup] Install them to enable all checks."
fi

echo "[setup] Done."
