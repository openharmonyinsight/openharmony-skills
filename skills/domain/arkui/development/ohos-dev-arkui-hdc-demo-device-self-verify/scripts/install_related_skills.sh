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

set -euo pipefail

RELATED_SKILL="ohos-dev-hdc-command-usage"
RELATED_PATH="skills/common/development/${RELATED_SKILL}"
RELATED_REPO="https://gitcode.com/openharmonyinsight/openharmony-skills.git"
RELATED_BRANCH="release"
MIN_VERSION="0.1.0"
PROBE_PATH="references/hdc-command-reference.md"

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${SKILLS_DIR:-${CODEX_HOME:-${HOME}/.codex}/skills}"
CHECK_ONLY=0

usage() {
    printf '%s\n' "Usage: install_related_skills.sh [--check] [--skills-dir DIR]"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --check)
            CHECK_ONLY=1
            ;;
        --skills-dir)
            shift
            [[ $# -gt 0 ]] || { usage; exit 2; }
            SKILLS_DIR="$1"
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            usage
            exit 2
            ;;
    esac
    shift
done

get_version() {
    awk '/^[[:space:]]+version:[[:space:]]*/ { gsub(/"/, "", $2); print $2; exit }' "$1"
}

version_gte() {
    [[ "$(printf '%s\n%s\n' "$2" "$1" | sort -V | head -n 1)" == "$2" ]]
}

is_compatible() {
    [[ -f "${TARGET_DIR}/SKILL.md" && -f "${TARGET_DIR}/${PROBE_PATH}" ]] || return 1
    local version
    version="$(get_version "${TARGET_DIR}/SKILL.md")"
    [[ -n "$version" ]] && version_gte "$version" "$MIN_VERSION"
}

TARGET_DIR="${SKILLS_DIR}/${RELATED_SKILL}"
if is_compatible; then
    printf '[OK] %s >= %s is indexed at %s\n' "$RELATED_SKILL" "$MIN_VERSION" "$TARGET_DIR"
    exit 0
fi

if [[ "$CHECK_ONLY" -eq 1 ]]; then
    printf '[MISSING] compatible %s >= %s is not indexed under %s\n' \
        "$RELATED_SKILL" "$MIN_VERSION" "$SKILLS_DIR" >&2
    exit 1
fi

SOURCE_DIR=""
REPO_ROOT="$(git -C "$SKILL_ROOT" rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -n "$REPO_ROOT" && -f "${REPO_ROOT}/${RELATED_PATH}/SKILL.md" ]]; then
    SOURCE_DIR="${REPO_ROOT}/${RELATED_PATH}"
else
    TMP_DIR="$(mktemp -d)"
    trap 'rm -rf "$TMP_DIR"' EXIT
    git clone --depth 1 --branch "$RELATED_BRANCH" --filter=blob:none --sparse \
        "$RELATED_REPO" "${TMP_DIR}/repo"
    git -C "${TMP_DIR}/repo" sparse-checkout set "$RELATED_PATH"
    SOURCE_DIR="${TMP_DIR}/repo/${RELATED_PATH}"
fi

[[ -f "${SOURCE_DIR}/SKILL.md" ]] || {
    printf '[ERROR] dependency source is missing SKILL.md: %s\n' "$SOURCE_DIR" >&2
    exit 1
}

mkdir -p "$TARGET_DIR"
cp -a "${SOURCE_DIR}/." "$TARGET_DIR/"
printf 'source=%s\nbranch=%s\npath=%s\n' \
    "$RELATED_REPO" "$RELATED_BRANCH" "$RELATED_PATH" > "${TARGET_DIR}/.install-source"

is_compatible || {
    printf '[ERROR] failed to install %s\n' "$RELATED_SKILL" >&2
    exit 1
}

printf '[OK] installed and indexed %s >= %s at %s\n' \
    "$RELATED_SKILL" "$MIN_VERSION" "$TARGET_DIR"
