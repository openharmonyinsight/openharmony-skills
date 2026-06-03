#!/usr/bin/env bash

set -euo pipefail

find_arkweb_root() {
  local dir="${1:-$PWD}"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/build_arkweb.sh" && -f "$dir/src/arkweb/build/build.sh" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

PRODUCT="${1:-rk3568_64}"
ROOT_HINT="${2:-$PWD}"

if ! ARKWEB_ROOT="$(find_arkweb_root "$ROOT_HINT")"; then
  echo "ArkWeb root not found from: $ROOT_HINT" >&2
  echo "Usage: $0 [product] [arkweb-root-or-subdir]" >&2
  exit 1
fi

BUILD_LOG="$ARKWEB_ROOT/src/out/$PRODUCT/build.log"

if [[ ! -f "$BUILD_LOG" ]]; then
  echo "Build log not found: $BUILD_LOG" >&2
  exit 1
fi

echo "ArkWeb root: $ARKWEB_ROOT"
echo "Product: $PRODUCT"
echo "Build log: $BUILD_LOG"
echo

echo "== First key error lines =="
grep -niE 'error:|fatal error|undefined reference|multiple definition|ERROR at|ninja: error|No such file|cannot find|killed|OutOfMemory|Package .* not found|Failed to extract|not in gzip format|not a tar archive|End-of-central-directory signature not found' "$BUILD_LOG" | head -20 || true
echo

echo "== Recent error lines =="
grep -ni 'error:' "$BUILD_LOG" | tail -20 || true
echo

echo "== Recent fatal or linker lines =="
grep -niE 'fatal error|undefined reference|multiple definition|ERROR at' "$BUILD_LOG" | tail -20 || true
echo

echo "== Recent missing-file or resource lines =="
grep -niE 'No such file|cannot find|killed|OutOfMemory' "$BUILD_LOG" | tail -20 || true
