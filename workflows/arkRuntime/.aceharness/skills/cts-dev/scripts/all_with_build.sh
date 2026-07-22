#!/usr/bin/env bash
set -x
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/style.sh"
"$SCRIPT_DIR/build_diff.sh"
"$SCRIPT_DIR/ut.sh"
"$SCRIPT_DIR/astcheck.sh"
"$SCRIPT_DIR/recheck.sh"
"$SCRIPT_DIR/parser.sh"
"$SCRIPT_DIR/runtime.sh"
"$SCRIPT_DIR/cts2.sh"
