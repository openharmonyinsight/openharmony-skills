#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
init_common
detect_build_dir_name "$STATIC_CORE"

rm -rf /tmp/ets && cd "$STATIC_CORE" && tests/tests-u-runner/runner.sh --ets-runtime --es2panda-debug-info --show-progress --build-dir "$BUILD_DIR_NAME" --processes=all
