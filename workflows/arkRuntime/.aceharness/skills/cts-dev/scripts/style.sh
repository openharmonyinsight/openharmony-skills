#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
init_common
detect_build_dir "$STATIC_CORE"

cd "$BUILD_DIR"
ninja clang-force-format
