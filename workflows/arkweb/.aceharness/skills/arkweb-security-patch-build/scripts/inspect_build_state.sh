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

PRODUCT="${1:-}"
ROOT_HINT="${2:-$PWD}"

if ! ARKWEB_ROOT="$(find_arkweb_root "$ROOT_HINT")"; then
  echo "ArkWeb root not found from: $ROOT_HINT" >&2
  echo "Usage: $0 [product] [arkweb-root-or-subdir]" >&2
  exit 1
fi

OUT_ROOT="$ARKWEB_ROOT/src/out"

if [[ ! -d "$OUT_ROOT" ]]; then
  echo "Output directory not found: $OUT_ROOT" >&2
  exit 1
fi

collect_dirs() {
  if [[ -n "$PRODUCT" ]]; then
    printf '%s\n' "$OUT_ROOT/$PRODUCT"
  else
    find "$OUT_ROOT" -mindepth 1 -maxdepth 1 -type d | sort
  fi
}

echo "ArkWeb root: $ARKWEB_ROOT"
echo "Output root: $OUT_ROOT"
echo

while IFS= read -r dir; do
  [[ -d "$dir" ]] || continue
  name="$(basename "$dir")"
  echo "== $name =="
  if [[ -f "$dir/args.gn" ]]; then
    echo "args.gn: present"
    grep -E 'target_cpu|product_name|use_ohos_sdk_sysroot|is_debug|is_release_build' "$dir/args.gn" || true
  else
    echo "args.gn: missing"
  fi

  if [[ -f "$dir/build.log" ]]; then
    echo "build.log: present"
    echo "build.log size: $(du -h "$dir/build.log" | cut -f1)"
    echo "build.log mtime: $(stat -c '%y' "$dir/build.log")"
  else
    echo "build.log: missing"
  fi

  echo
done < <(collect_dirs)
