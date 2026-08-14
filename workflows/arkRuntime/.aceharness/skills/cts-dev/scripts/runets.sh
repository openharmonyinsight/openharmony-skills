#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
init_common
detect_build_dir "$STATIC_CORE"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <path-to.ets>" >&2
  exit 1
fi

ETS_FILE="$1"
STEM="$(basename "$ETS_FILE" .ets)"
OUTPUT="/tmp/${STEM}.abc"

"$BUILD_DIR/bin/es2panda" \
  --arktsconfig="$BUILD_DIR/tools/es2panda/generated/arktsconfig.json" \
  --gen-stdlib=false \
  --extension=ets \
  --opt-level=2 \
  --output="$OUTPUT" \
  "$ETS_FILE"
