#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

cmd=(build "$DOCS_DIR" -o "$BUILD_ROOT" --mode sidecar-only)

if [[ "${WIKI_AGENTIZER_FULL_BUILD:-0}" == "1" ]]; then
    cmd+=(--full)
fi

if [[ -n "${WIKI_AGENTIZER_CONFIG:-}" ]]; then
    cmd+=(--config "$WIKI_AGENTIZER_CONFIG")
fi

if [[ -n "${WIKI_AGENTIZER_JOBS:-}" ]]; then
    cmd+=(--jobs "$WIKI_AGENTIZER_JOBS")
fi

if [[ "${WIKI_AGENTIZER_STRICT:-0}" == "1" ]]; then
    cmd+=(--strict)
fi

if [[ "${WIKI_AGENTIZER_ENABLE_LLM:-0}" == "1" ]]; then
    cmd+=(--enable-llm)
fi

if [[ "${WIKI_AGENTIZER_DRY_RUN:-0}" == "1" ]]; then
    cmd+=(--dry-run)
fi

if [[ -n "${WIKI_AGENTIZER_LOG_LEVEL:-}" ]]; then
    cmd+=(--log-level "$WIKI_AGENTIZER_LOG_LEVEL")
fi

run_wiki_agentizer "${cmd[@]}"
promote_generated_agent
