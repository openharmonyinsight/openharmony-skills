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

is_lfs_pointer() {
  local file="$1"
  [[ -f "$file" ]] || return 1
  head -n 1 "$file" 2>/dev/null | LC_ALL=C grep -aFxq 'version https://git-lfs.github.com/spec/v1'
}

ROOT_HINT="${1:-$PWD}"

if ! ARKWEB_ROOT="$(find_arkweb_root "$ROOT_HINT")"; then
  echo "ArkWeb root not found from: $ROOT_HINT" >&2
  echo "Usage: $0 [arkweb-root-or-subdir]" >&2
  exit 1
fi

SRC_ROOT="$ARKWEB_ROOT/src"
INSTALL_FILE="$SRC_ROOT/ohos_sdk/.install"
ROOT_ATTR="$SRC_ROOT/.gitattributes"
SDK_ATTR="$SRC_ROOT/ohos_sdk/.gitattributes"
NDK_ATTR="$SRC_ROOT/third_party/ohos_ndk/.gitattributes"

declare -A seen
declare -A seen_patterns
required_files=()
optional_files=()
required_patterns=()
optional_patterns=()

add_required() {
  local rel="$1"
  [[ -n "$rel" ]] || return 0
  if [[ -z "${seen[$rel]:-}" ]]; then
    seen["$rel"]=1
    required_files+=("$rel")
  fi
}

add_optional() {
  local rel="$1"
  [[ -n "$rel" ]] || return 0
  if [[ -z "${seen[$rel]:-}" ]]; then
    seen["$rel"]=1
    optional_files+=("$rel")
  fi
}

add_pattern() {
  local bucket="$1"
  local pattern="$2"
  [[ -n "$pattern" ]] || return 0
  if [[ -z "${seen_patterns[$bucket:$pattern]:-}" ]]; then
    seen_patterns["$bucket:$pattern"]=1
    if [[ "$bucket" == "required" ]]; then
      required_patterns+=("$pattern")
    else
      optional_patterns+=("$pattern")
    fi
  fi
}

add_lfs_attr_entries() {
  local attr_file="$1"
  local rel_prefix="$2"
  local bucket="$3"
  [[ -f "$attr_file" ]] || return 0

  local raw rel pattern match
  while IFS= read -r raw; do
    raw="${raw%%#*}"
    raw="${raw%%[[:space:]]filter=lfs*}"
    raw="${raw#\"}"
    raw="${raw%\"}"
    raw="${raw#/}"
    [[ -n "$raw" ]] || continue

    if [[ -n "$rel_prefix" ]]; then
      rel="$rel_prefix/${raw#./}"
    else
      rel="${raw#./}"
    fi

    if [[ "$rel" == *"*"* || "$rel" == *"?"* || "$rel" == *"["* ]]; then
      pattern="$SRC_ROOT/$rel"
      while IFS= read -r match; do
        [[ -e "$match" ]] || continue
        if [[ "$bucket" == "required" ]]; then
          add_required "${match#"$SRC_ROOT/"}"
        else
          add_optional "${match#"$SRC_ROOT/"}"
        fi
      done < <(compgen -G "$pattern" || true)
      if ! compgen -G "$pattern" >/dev/null; then
        add_pattern "$bucket" "$rel"
      fi
    else
      if [[ "$bucket" == "required" ]]; then
        add_required "$rel"
      else
        add_optional "$rel"
      fi
    fi
  done < <(awk '!/^[[:space:]]*#/ && /filter=lfs/ {print $1 " filter=lfs"}' "$attr_file")
}

if [[ -f "$INSTALL_FILE" ]]; then
  while IFS= read -r package; do
    add_required "ohos_sdk/$package"
  done < <(sed -n 's/^[[:space:]]*prebuilts_[a-z_]*_path="\([^"]*\)".*/\1/p' "$INSTALL_FILE")
fi

add_required "build/pgo/ohos/arkweb.profdata"
add_lfs_attr_entries "$ROOT_ATTR" "" "required"
add_lfs_attr_entries "$SDK_ATTR" "ohos_sdk" "required"
add_lfs_attr_entries "$NDK_ATTR" "third_party/ohos_ndk" "optional"

echo "ArkWeb root: $ARKWEB_ROOT"
echo "Relevant LFS config files:"
echo "  - $ROOT_ATTR"
echo "  - $SDK_ATTR"
echo "  - $NDK_ATTR"
echo "  - $INSTALL_FILE"
echo

total=0
ok_count=0
missing_count=0
pointer_count=0
optional_total=0
optional_ok_count=0
optional_missing_count=0
optional_pointer_count=0
required_unmatched_pattern_count=0
optional_unmatched_pattern_count=0

for rel in "${required_files[@]}"; do
  abs="$SRC_ROOT/$rel"
  total=$((total + 1))
  if [[ ! -e "$abs" ]]; then
    echo "MISSING   $rel"
    missing_count=$((missing_count + 1))
    continue
  fi

  if is_lfs_pointer "$abs"; then
    echo "POINTER   $rel"
    pointer_count=$((pointer_count + 1))
    continue
  fi

  size="$(stat -c %s "$abs" 2>/dev/null || wc -c < "$abs")"
  echo "OK        $rel ($size bytes)"
  ok_count=$((ok_count + 1))
done

if ((${#optional_files[@]} > 0)); then
  echo
  echo "Optional LFS entries (informational only):"
  for rel in "${optional_files[@]}"; do
    abs="$SRC_ROOT/$rel"
    optional_total=$((optional_total + 1))
    if [[ ! -e "$abs" ]]; then
      echo "MISSING   $rel"
      optional_missing_count=$((optional_missing_count + 1))
      continue
    fi

    if is_lfs_pointer "$abs"; then
      echo "POINTER   $rel"
      optional_pointer_count=$((optional_pointer_count + 1))
      continue
    fi

    size="$(stat -c %s "$abs" 2>/dev/null || wc -c < "$abs")"
    echo "OK        $rel ($size bytes)"
    optional_ok_count=$((optional_ok_count + 1))
  done
fi

if ((${#required_patterns[@]} > 0)); then
  echo
  echo "Required LFS patterns with no current file matches:"
  for rel in "${required_patterns[@]}"; do
    echo "WARN_PATTERN $rel"
    required_unmatched_pattern_count=$((required_unmatched_pattern_count + 1))
  done
fi

if ((${#optional_patterns[@]} > 0)); then
  echo
  echo "Optional LFS patterns with no current file matches:"
  for rel in "${optional_patterns[@]}"; do
    echo "WARN_PATTERN $rel"
    optional_unmatched_pattern_count=$((optional_unmatched_pattern_count + 1))
  done
fi

echo
echo "Required summary: total=$total ok=$ok_count missing=$missing_count pointer=$pointer_count"
if (( optional_total > 0 )); then
  echo "Optional summary: total=$optional_total ok=$optional_ok_count missing=$optional_missing_count pointer=$optional_pointer_count"
fi
if (( required_unmatched_pattern_count > 0 || optional_unmatched_pattern_count > 0 )); then
  echo "Unmatched LFS patterns: required=$required_unmatched_pattern_count optional=$optional_unmatched_pattern_count"
fi
echo
echo "Optional manual inspection:"
echo "  git -C $SRC_ROOT lfs ls-files | rg 'ohos_sdk|third_party/ohos_ndk|build/pgo/ohos/arkweb.profdata'"
echo

if (( missing_count > 0 || pointer_count > 0 )); then
  echo "Detected missing or non-materialized LFS assets."
  echo "Recommended fix:"
  echo "  cd $ARKWEB_ROOT"
  echo "  repo forall -c 'git lfs pull'"
  echo
  echo "Or current repo only:"
  echo "  git -C $SRC_ROOT lfs pull"
  exit 2
fi

echo "No missing required LFS asset or LFS pointer file was detected in the checked ArkWeb prebuilts."
