#!/usr/bin/env bash

# ArkWeb Build Error Analyzer (simplified)
# Analyzes build.log and outputs structured error report.
# Usage:
#   $0 [product] [arkweb-root-or-subdir]
#   $0 <build.log> [arkweb-root-or-subdir]

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

usage() {
  echo "Usage: $0 [product] [arkweb-root-or-subdir]" >&2
  echo "       $0 <build.log> [arkweb-root-or-subdir]" >&2
}

PRODUCT="${1:-rk3568_64}"
ROOT_HINT="${2:-$PWD}"
BUILD_LOG=""

if [[ "${1:-}" == *.log ]]; then
  BUILD_LOG="$1"
  if [[ "$BUILD_LOG" != /* ]]; then
    BUILD_LOG="$(cd "$(dirname "$BUILD_LOG")" && pwd)/$(basename "$BUILD_LOG")"
  fi
  if ! ARKWEB_ROOT="$(find_arkweb_root "$ROOT_HINT")"; then
    if [[ "$BUILD_LOG" == */src/out/*/build.log ]]; then
      ROOT_HINT="${BUILD_LOG%%/src/out/*/build.log}"
    fi
    if ! ARKWEB_ROOT="$(find_arkweb_root "$ROOT_HINT")"; then
      echo "ArkWeb root not found from: $ROOT_HINT" >&2
      usage
      exit 1
    fi
  fi
  PRODUCT="$(basename "$(dirname "$BUILD_LOG")")"
else
  if ! ARKWEB_ROOT="$(find_arkweb_root "$ROOT_HINT")"; then
    echo "ArkWeb root not found from: $ROOT_HINT" >&2
    usage
    exit 1
  fi
  BUILD_LOG="$ARKWEB_ROOT/src/out/$PRODUCT/build.log"
fi

KEY_ERROR_REGEX='error:|fatal error|undefined reference|multiple definition|ERROR at|ninja: error|No such file|cannot find|killed|OutOfMemory|Package .* not found|Failed to extract|not in gzip format|not a tar archive|End-of-central-directory signature not found'

if [[ ! -f "$BUILD_LOG" ]]; then
  echo "Build log not found: $BUILD_LOG" >&2
  echo
  echo "Available output directories:"
  find "$ARKWEB_ROOT/src/out" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort || true
  exit 1
fi

echo "ArkWeb root: $ARKWEB_ROOT"
echo "Product: $PRODUCT"
echo "Build log: $BUILD_LOG"
echo "File size: $(du -h "$BUILD_LOG" | cut -f1)"
echo "Last modified: $(stat -c '%y' "$BUILD_LOG")"
echo

echo "== Error counters =="
printf 'error: %s\n' "$(grep -c -i 'error:' "$BUILD_LOG" || true)"
printf 'fatal: %s\n' "$(grep -c -i 'fatal error' "$BUILD_LOG" || true)"
printf 'undefined reference: %s\n' "$(grep -c 'undefined reference' "$BUILD_LOG" || true)"
printf 'multiple definition: %s\n' "$(grep -c 'multiple definition' "$BUILD_LOG" || true)"
printf 'gn errors: %s\n' "$(grep -c 'ERROR at //' "$BUILD_LOG" || true)"
printf 'ninja target/graph errors: %s\n' "$(grep -c -iE 'ninja: error:.*(unknown target|loading .*\.ninja|build\.ninja)' "$BUILD_LOG" || true)"
printf 'killed/oom: %s\n' "$(grep -c -iE 'killed|OutOfMemory' "$BUILD_LOG" || true)"
echo

classify_stage() {
  if grep -qiE 'Package .* not found|Failed to extract|not in gzip format|not a tar archive|End-of-central-directory signature not found|unzip: cannot find|prebuilts_.*_path' "$BUILD_LOG"; then
    echo "pre-gn/sdk-lfs"
    return 0
  fi
  if grep -q 'ERROR at //' "$BUILD_LOG"; then
    echo "gn-generation"
    return 0
  fi
  if grep -qiE 'ninja: error:.*(unknown target|loading .*\.ninja|build\.ninja)' "$BUILD_LOG"; then
    echo "ninja-graph-or-target"
    return 0
  fi
  if grep -qE 'FAILED:|fatal error:|undefined reference|multiple definition|ld.lld: error|clang(\+\+)?: error|collect2: error' "$BUILD_LOG"; then
    echo "ninja-compile-link"
    return 0
  fi
  if grep -qiE 'killed|OutOfMemory' "$BUILD_LOG"; then
    echo "resource-or-terminated"
    return 0
  fi
  if tail -80 "$BUILD_LOG" | grep -qE '^\[[0-9]+/[0-9]+\]' && ! grep -qE 'FAILED:|ERROR at //|ninja: error' "$BUILD_LOG"; then
    echo "resource-or-terminated-suspected"
    return 0
  fi
  echo "unknown"
}

STAGE="$(classify_stage)"
echo "== Failure stage classification =="
echo "stage: $STAGE"
echo

echo "== Recent key error lines =="
grep -niE "$KEY_ERROR_REGEX" "$BUILD_LOG" | tail -40 || true
echo

FIRST_LINE="$(grep -niE "$KEY_ERROR_REGEX" "$BUILD_LOG" | head -1 | cut -d: -f1 || true)"
LAST_LINE="$(grep -niE "$KEY_ERROR_REGEX" "$BUILD_LOG" | tail -1 | cut -d: -f1 || true)"

if [[ -n "$FIRST_LINE" ]]; then
  START=$(( FIRST_LINE > 20 ? FIRST_LINE - 20 : 1 ))
  END=$(( FIRST_LINE + 20 ))
  echo "== Context around the first key error =="
  sed -n "${START},${END}p" "$BUILD_LOG"
  if [[ -n "$LAST_LINE" && "$LAST_LINE" != "$FIRST_LINE" ]]; then
    START=$(( LAST_LINE > 10 ? LAST_LINE - 10 : 1 ))
    END=$(( LAST_LINE + 10 ))
    echo
    echo "== Context around the last key error =="
    sed -n "${START},${END}p" "$BUILD_LOG"
  fi
else
  echo "== Log tail (no matched key errors) =="
  tail -200 "$BUILD_LOG"
fi
