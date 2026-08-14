#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

[[ -f "$AGENT_DIR/manifest.json" ]] || fail "generated index not found: $AGENT_DIR/manifest.json. Run ./scripts/build_agent.sh first."

run_wiki_agentizer validate "$SKILL_DIR"
