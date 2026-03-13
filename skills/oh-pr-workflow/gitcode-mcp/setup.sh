#!/usr/bin/env bash
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# setup.sh — Install gitcode-mcp and register as Claude Code MCP server
#
# Strategy:
#   1. Try embedded pre-built binary (bin/gitcode-mcp-linux-amd64)
#   2. If it doesn't run (wrong arch/OS) → compile from source (requires Go)
#
# Usage: bash setup.sh [--force]

set -euo pipefail

# Load user's full PATH from their interactive login shell
# (bash scripts don't inherit .zshrc/.bashrc PATH, so installed tools may not be found)
# -i: interactive (loads .bashrc/.zshrc), -l: login (loads .bash_profile/.zprofile)
USER_PATH="$("${SHELL:-/bin/bash}" -i -l -c 'echo $PATH' 2>/dev/null)" || true
if [[ -n "${USER_PATH}" ]]; then
    export PATH="${USER_PATH}:${PATH}"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BINARY_NAME="gitcode-mcp"
INSTALL_DIR="${HOME}/go/bin"
INSTALL_PATH="${INSTALL_DIR}/${BINARY_NAME}"
SOURCE_HASH_FILE="${SCRIPT_DIR}/.source-hash"
BINARY_HASH_FILE="${SCRIPT_DIR}/.binary-hash"
FORCE=false

if [[ "${1:-}" == "--force" ]]; then
    FORCE=true
fi

# --- Version tracking ---

source_hash() {
    find "${SCRIPT_DIR}" -name "*.go" -o -name "go.mod" -o -name "go.sum" | sort | xargs cat | md5sum | cut -d' ' -f1
}

binary_hash() {
    if [[ -f "${INSTALL_PATH}" ]]; then
        md5sum "${INSTALL_PATH}" | cut -d' ' -f1
    else
        echo "none"
    fi
}

needs_install() {
    if [[ ! -f "${INSTALL_PATH}" ]]; then
        echo "binary not found"
        return 0
    fi
    if [[ ! -f "${SOURCE_HASH_FILE}" ]] || [[ ! -f "${BINARY_HASH_FILE}" ]]; then
        echo "no version tracking files"
        return 0
    fi
    local current_src=$(source_hash)
    local saved_src=$(cat "${SOURCE_HASH_FILE}")
    if [[ "${current_src}" != "${saved_src}" ]]; then
        echo "source changed (${saved_src:0:8} → ${current_src:0:8})"
        return 0
    fi
    local current_bin=$(binary_hash)
    local saved_bin=$(cat "${BINARY_HASH_FILE}")
    if [[ "${current_bin}" != "${saved_bin}" ]]; then
        echo "binary was replaced externally"
        return 0
    fi
    return 1
}

# --- Check if install needed ---

if [[ "${FORCE}" == "false" ]]; then
    REASON=$(needs_install) || true
    if [[ -z "${REASON}" ]]; then
        echo "[OK] gitcode-mcp is up to date (source: $(cat "${SOURCE_HASH_FILE}" | head -c 8))"
        # Still check MCP registration
        if command -v claude &>/dev/null; then
            if ! claude mcp list 2>/dev/null | grep -q "gitcode:.*Connected"; then
                echo "[WARN] MCP not registered or disconnected, re-registering..."
            else
                exit 0
            fi
        else
            exit 0
        fi
    else
        echo "[INFO] Install needed: ${REASON}"
    fi
fi

# --- Install binary ---

mkdir -p "${INSTALL_DIR}"

install_embedded() {
    local EMBEDDED="${SCRIPT_DIR}/bin/gitcode-mcp-linux-amd64"
    if [[ ! -f "${EMBEDDED}" ]]; then
        return 1
    fi

    # Check platform compatibility via file command (don't try to run — it's a stdio server that blocks)
    local OS=$(uname -s)
    local ARCH=$(uname -m)
    if [[ "${OS}" != "Linux" ]]; then
        echo "[INFO] Embedded binary is Linux-only, this is ${OS}"
        return 1
    fi
    if [[ "${ARCH}" != "x86_64" ]]; then
        echo "[INFO] Embedded binary is x86_64, this is ${ARCH}"
        return 1
    fi

    cp "${EMBEDDED}" "${INSTALL_PATH}"
    chmod +x "${INSTALL_PATH}"
    echo "[OK] Installed from embedded binary (linux-amd64)"
    return 0
}

install_from_source() {
    # Check Go
    if ! command -v go &>/dev/null; then
        for GO_PATH in /usr/local/go/bin/go "${HOME}/go-install/go/bin/go"; do
            if [[ -f "${GO_PATH}" ]]; then
                export PATH="$(dirname "${GO_PATH}"):${PATH}"
                break
            fi
        done
    fi
    if ! command -v go &>/dev/null; then
        echo "[ERROR] Go is not installed and embedded binary is incompatible."
        echo "  Install Go 1.22+: https://go.dev/dl/"
        exit 1
    fi
    echo "[INFO] Using Go: $(go version)"
    echo "[INFO] Building from source..."
    cd "${SCRIPT_DIR}"
    CGO_ENABLED=0 go build -o "${INSTALL_PATH}" . 2>&1
    if [[ $? -ne 0 ]]; then
        echo "[ERROR] Build failed"
        exit 1
    fi
    echo "[OK] Built from source"
}

# Try embedded first, fall back to source
install_embedded || install_from_source

# Save version hashes
source_hash > "${SOURCE_HASH_FILE}"
binary_hash > "${BINARY_HASH_FILE}"
echo "[OK] Installed to ${INSTALL_PATH}"

# --- Register MCP server for detected agents ---

GITCODE_TOKEN=$(git config --get gitcode.token 2>/dev/null || echo "")
if [[ -z "${GITCODE_TOKEN}" ]]; then
    echo "[WARN] No gitcode.token in git config. Set it with:"
    echo "  git config --global gitcode.token YOUR_TOKEN"
    GITCODE_TOKEN="PLEASE_SET_TOKEN"
fi

REGISTERED=false

# Claude Code
if command -v claude &>/dev/null; then
    claude mcp remove gitcode -s user 2>/dev/null || true
    claude mcp add gitcode -s user \
        -e "GITCODE_TOKEN=${GITCODE_TOKEN}" \
        -- "${INSTALL_PATH}" 2>/dev/null
    echo "[OK] Registered in Claude Code"
    REGISTERED=true
fi

# OpenCode
if command -v opencode &>/dev/null; then
    # Find existing OpenCode config (check in priority order)
    OPENCODE_CONFIG=""
    XDG_DIR="${XDG_CONFIG_HOME:-${HOME}/.config}"
    for candidate in \
        "${XDG_DIR}/opencode/opencode.json" \
        "${HOME}/.opencode.json" \
        "${HOME}/.opencode/config.json"; do
        if [[ -f "${candidate}" ]]; then
            OPENCODE_CONFIG="${candidate}"
            break
        fi
    done

    # No existing config found → create at XDG standard location
    if [[ -z "${OPENCODE_CONFIG}" ]]; then
        OPENCODE_CONFIG="${XDG_DIR}/opencode/opencode.json"
        mkdir -p "$(dirname "${OPENCODE_CONFIG}")"
    fi

    # Inject MCP config via text manipulation (preserves comments, trailing commas, formatting)
    MCP_BLOCK='  "mcp": {
    "gitcode": {
      "type": "local",
      "command": ["'"${INSTALL_PATH}"'"],
      "environment": { "GITCODE_TOKEN": "'"${GITCODE_TOKEN}"'" },
      "enabled": true
    }
  }'
    python3 -c "
import re, sys

config_path = '${OPENCODE_CONFIG}'
mcp_block = '''${MCP_BLOCK}'''

with open(config_path) as f:
    text = f.read()

# Check if mcp.gitcode already exists
if '\"gitcode\"' in text and '\"mcp\"' in text:
    # Replace existing gitcode block inside mcp
    # Match from '\"gitcode\"' to the next closing '}' after 'enabled'
    text = re.sub(
        r'\"gitcode\"\s*:\s*\{[^}]*\{[^}]*\}[^}]*\}',
        '\"gitcode\": {\n      \"type\": \"local\",\n      \"command\": [\"${INSTALL_PATH}\"],\n      \"environment\": { \"GITCODE_TOKEN\": \"${GITCODE_TOKEN}\" },\n      \"enabled\": true\n    }',
        text, count=1)
elif '\"mcp\"' in text:
    # mcp exists but no gitcode — insert gitcode into mcp block
    text = re.sub(
        r'(\"mcp\"\s*:\s*\{)',
        r'\1\n    \"gitcode\": {\n      \"type\": \"local\",\n      \"command\": [\"${INSTALL_PATH}\"],\n      \"environment\": { \"GITCODE_TOKEN\": \"${GITCODE_TOKEN}\" },\n      \"enabled\": true\n    },',
        text, count=1)
else:
    # No mcp section — insert before the last closing brace
    last_brace = text.rfind('}')
    if last_brace > 0:
        # Check if we need a comma before mcp
        before = text[:last_brace].rstrip()
        comma = '' if before.endswith(',') or before.endswith('{') else ','
        text = before + comma + '\n' + mcp_block + '\n}'

with open(config_path, 'w') as f:
    f.write(text)
" 2>/dev/null

    echo "[OK] Registered in OpenCode (${OPENCODE_CONFIG})"
    REGISTERED=true
fi

if [[ "${REGISTERED}" == "false" ]]; then
    echo "[INFO] No supported agent CLI found. Register manually:"
    echo ""
    echo "  Claude Code:"
    echo "    claude mcp add gitcode -s user -e GITCODE_TOKEN=xxx -- ${INSTALL_PATH}"
    echo ""
    echo "  OpenCode (add to ~/.config/opencode/opencode.json):"
    echo '    {"mcp":{"gitcode":{"type":"local","command":["'${INSTALL_PATH}'"],"environment":{"GITCODE_TOKEN":"xxx"}}}}'
fi

echo "[DONE] Setup complete. Restart your agent session to load MCP tools."
