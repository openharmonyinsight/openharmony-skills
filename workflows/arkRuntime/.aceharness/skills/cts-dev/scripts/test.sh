#!/usr/bin/env bash
set -e
set -o pipefail

CURRENT_STEP=""
trap 'err=$?; echo ""; echo "ERROR: Step \"${CURRENT_STEP}\" failed at line ${BASH_LINENO[0]:-?} with exit code $err" >&2; exit $err' ERR

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
init_common
detect_build_dir "$STATIC_CORE"

TESTS_DIR="$STATIC_CORE/tests"

CURRENT_STEP="clang-force-format"
echo "=== Running $CURRENT_STEP ==="
pushd "$BUILD_DIR" && ninja clang-force-format && popd

CURRENT_STEP="ETS CTS tests"
echo "=== Running $CURRENT_STEP ==="
"$TESTS_DIR/tests-u-runner/runner.sh" --ets-cts --es2panda-debug-info --show-progress --build-dir "$BUILD_DIR" --processes=all

CURRENT_STEP="parser tests"
echo "=== Running $CURRENT_STEP ==="
"$TESTS_DIR/tests-u-runner/runner.sh" --parser --es2panda-debug-info --no-js --show-progress --build-dir "$BUILD_DIR" --processes=all

CURRENT_STEP="ETS runtime tests"
echo "=== Running $CURRENT_STEP ==="
"$TESTS_DIR/tests-u-runner/runner.sh" --ets-runtime --es2panda-debug-info --show-progress --build-dir "$BUILD_DIR" --processes=all

CURRENT_STEP="astchecker tests"
echo "=== Running $CURRENT_STEP ==="
"$TESTS_DIR/tests-u-runner/runner.sh" --astchecker --es2panda-debug-info --no-js --show-progress --build-dir "$BUILD_DIR" --processes=all

CURRENT_STEP="srcdumper tests"
echo "=== Running $CURRENT_STEP ==="
"$TESTS_DIR/tests-u-runner/runner.sh" --srcdumper --es2panda-debug-info --no-js --show-progress --build-dir "$BUILD_DIR" --processes=all --workdir="$STATIC_CORE/tools/es2panda/test/test-lists/srcdumper"

CURRENT_STEP=""
echo "=== All steps completed ==="
