#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
init_common
detect_build_dir_name "$STATIC_CORE"

RUN_WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/ets-runtime.XXXXXX")"
RUN_MARKER="$RUN_WORKDIR/.cts-dev-owner"
printf '%s\n' "$$" > "$RUN_MARKER"

cleanup() {
    if [[ -f "$RUN_MARKER" && "$(cat "$RUN_MARKER")" == "$$" &&
        "$RUN_WORKDIR" == "${TMPDIR:-/tmp}/ets-runtime."* ]]; then
        rm -rf -- "$RUN_WORKDIR"
    fi
}
trap cleanup EXIT

cd "$STATIC_CORE"
tests/tests-u-runner/runner.sh --ets-runtime --es2panda-debug-info --show-progress \
    --build-dir "$BUILD_DIR" --processes=all --workdir="$RUN_WORKDIR"
