#!/bin/bash
# Build wrapper for OpenHarmony ace_engine builds with PID tracking.
# Usage: build_wrapper.sh --product <name> -- [build.sh args...]
#
# This script:
#   1. Writes BUILD_PID=<pid> as the first line of build_console.log
#   2. Launches build.sh in a detached process group (survives subagent cleanup)
#   3. Appends all build output to build_console.log
#
# The PID line enables monitor_progress.sh to verify the process is alive.

set -euo pipefail

PRODUCT_NAME=""
BUILD_ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --product)
            PRODUCT_NAME="$2"
            shift 2
            ;;
        --)
            shift
            BUILD_ARGS=("$@")
            break
            ;;
        *)
            echo "Error: Unknown option '$1'" >&2
            echo "Usage: build_wrapper.sh --product <name> -- [build.sh args...]" >&2
            exit 1
            ;;
    esac
done

if [[ -z "$PRODUCT_NAME" ]]; then
    echo "Error: --product is required" >&2
    exit 1
fi

# Auto-detect OpenHarmony root
OH_ROOT="$(pwd)"
while [[ ! -f "$OH_ROOT/.gn" ]]; do
    OH_ROOT="$(dirname "$OH_ROOT")"
    if [[ "$OH_ROOT" == "/" ]]; then
        echo "Error: OpenHarmony root not found (no .gn file)" >&2
        exit 1
    fi
done

# Determine output directory (handle special cases)
if [[ "$PRODUCT_NAME" == "ohos-sdk" ]]; then
    OUT_DIR="$OH_ROOT/out/sdk"
elif [[ "$PRODUCT_NAME" == "host_product" ]]; then
    OUT_DIR="$OH_ROOT/out/host/host_product"
else
    OUT_DIR="$OH_ROOT/out/$PRODUCT_NAME"
fi

BUILD_LOG="$OUT_DIR/build_console.log"

# Ensure output directory exists
mkdir -p "$OUT_DIR"

# Launch build in detached process group
# Auto-inject --product-name if not already in BUILD_ARGS
HAS_PRODUCT_NAME=false
for arg in "${BUILD_ARGS[@]}"; do
    if [[ "$arg" == "--product-name" ]]; then
        HAS_PRODUCT_NAME=true
        break
    fi
done
if [[ "$HAS_PRODUCT_NAME" == false ]]; then
    BUILD_ARGS=("--product-name" "$PRODUCT_NAME" "${BUILD_ARGS[@]}")
fi

cd "$OH_ROOT"

# setsid forks a child process — $! only captures the setsid parent PID which
# exits immediately. To track the real build.sh PID, we write $$ from inside
# the setsid session, then exec build.sh so it inherits that same PID.
setsid bash -c '
    echo "BUILD_PID=$$"
    exec ./build.sh "$@"
' _ "${BUILD_ARGS[@]}" > "$BUILD_LOG" 2>&1 &

# Wait briefly for the child to write its PID line
sleep 0.3
BUILD_PID=$(head -1 "$BUILD_LOG" 2>/dev/null | grep -oP '^BUILD_PID=\K\d+' || echo "unknown")

echo "Build PID: $BUILD_PID"
echo "Log: $BUILD_LOG"
echo ""
echo "编译已启动。如需监听编译进度，在终端运行："
echo "bash $(dirname "$0")/monitor_progress.sh --root $OH_ROOT --product $PRODUCT_NAME"
