#!/usr/bin/env bash

if [[ -n "${SPEC_TEST_ANALYZER_COMMON_SH:-}" ]]; then
    return 0
fi
SPEC_TEST_ANALYZER_COMMON_SH=1

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SKILL_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
DOCS_DIR="$SKILL_DIR/docs"
AGENT_DIR="$SKILL_DIR/.agent"
TOOLING_DIR="$SKILL_DIR/.tooling"
TOOL_REPO_DIR_DEFAULT="$TOOLING_DIR/wiki_agentizer"
TOOL_REPO_DIR="${WIKI_AGENTIZER_DIR:-$TOOL_REPO_DIR_DEFAULT}"
VENV_DIR="$TOOLING_DIR/wiki_agentizer-venv"
BUILD_ROOT="$TOOLING_DIR/wiki_agentizer-build"
BUILD_AGENT_DIR="$BUILD_ROOT/.agent"
PYTHON_BIN="${PYTHON_BIN:-python3}"
WIKI_AGENTIZER_REPO="${WIKI_AGENTIZER_REPO:-https://gitcode.com/anxuesm/wiki_agentizer}"
WIKI_AGENTIZER_REF="${WIKI_AGENTIZER_REF:-}"

fail() {
    printf 'error: %s\n' "$*" >&2
    exit 1
}

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || fail "missing required command: $1"
}

ensure_docs_dir() {
    [[ -d "$DOCS_DIR" ]] || fail "docs directory not found: $DOCS_DIR"
}

clone_wiki_agentizer() {
    if [[ -d "$TOOL_REPO_DIR/.git" ]] || [[ -f "$TOOL_REPO_DIR/pyproject.toml" ]]; then
        return 0
    fi

    mkdir -p "$TOOLING_DIR"
    git clone "$WIKI_AGENTIZER_REPO" "$TOOL_REPO_DIR"

    if [[ -n "$WIKI_AGENTIZER_REF" ]]; then
        git -C "$TOOL_REPO_DIR" checkout "$WIKI_AGENTIZER_REF"
    fi
}

ensure_wiki_agentizer() {
    ensure_docs_dir
    require_cmd git
    require_cmd "$PYTHON_BIN"

    clone_wiki_agentizer
    [[ -f "$TOOL_REPO_DIR/pyproject.toml" ]] || fail "wiki_agentizer checkout is missing pyproject.toml: $TOOL_REPO_DIR"

    if [[ ! -x "$VENV_DIR/bin/python" ]]; then
        "$PYTHON_BIN" -m venv "$VENV_DIR"
    fi

    if [[ "${WIKI_AGENTIZER_FORCE_REINSTALL:-0}" == "1" ]] || \
       ! "$VENV_DIR/bin/python" -c "import wiki_agentizer" >/dev/null 2>&1; then
        "$VENV_DIR/bin/python" -m pip install -e "$TOOL_REPO_DIR"
    fi
}

run_wiki_agentizer() {
    ensure_wiki_agentizer
    PYTHONPATH="$TOOL_REPO_DIR${PYTHONPATH:+:$PYTHONPATH}" \
        "$VENV_DIR/bin/python" -m wiki_agentizer.cli.main "$@"
}

promote_generated_agent() {
    [[ -f "$BUILD_AGENT_DIR/manifest.json" ]] || fail "generated manifest not found: $BUILD_AGENT_DIR/manifest.json"

    if [[ -d "$AGENT_DIR" ]]; then
        mv "$AGENT_DIR" "$SKILL_DIR/.agent.prev.$(date +%s)"
    fi

    mv "$BUILD_AGENT_DIR" "$AGENT_DIR"
}
