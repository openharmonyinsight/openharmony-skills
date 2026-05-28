#!/bin/bash
# Show ArkWeb git changes after filtering expected default dirty entries.

set -euo pipefail

declare -a IGNORE_PREFIXES=()
declare -A IGNORE_EXACT_MAP=()
SHOW_ALL=0
declare -a BUILTIN_IGNORE_PREFIXES=(
  "third_party/rust-toolchain"
  "third_party/rust/chromium_crates_io"
)
declare -a BUILTIN_SRC_EXACT_IGNORES=(
  "third_party/ohos_ndk/includes/ohos_adapter/screenlock_manager_adapter.h"
  "third_party/ohos_nweb_hap/hvigor/"
  "third_party/ohos_nweb_hap/signature/"
)
declare -a BUILTIN_ARKWEB_EXACT_IGNORES=(
  "build/search_engines/prepopulated_engines.json"
)

find_arkweb_root() {
  local dir="${1:-$PWD}"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/build_arkweb.sh" && -f "$dir/src/arkweb/build/build.sh" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  echo "ArkWeb root not found" >&2
  return 1
}

trim_spaces() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

normalize_path() {
  local path
  path="$(trim_spaces "$1")"
  path="${path#./}"
  path="${path%\"}"
  path="${path#\"}"
  printf '%s' "$path"
}

is_prefixed_path() {
  local path="$1"
  local prefix="$2"
  [[ "$path" == "$prefix" || "$path" == "$prefix/"* ]]
}

append_unique_prefix() {
  local value="$1"
  [[ -z "$value" ]] && return 0
  local existing
  for existing in "${IGNORE_PREFIXES[@]:-}"; do
    [[ "$existing" == "$value" ]] && return 0
  done
  IGNORE_PREFIXES+=("$value")
}

set_exact_ignore() {
  local value="$1"
  [[ -z "$value" ]] && return 0
  if [[ "$value" == */ ]]; then
    append_unique_prefix "${value%/}"
    return 0
  fi
  IGNORE_EXACT_MAP["$value"]=1
}

load_builtin_ignores() {
  local repo_kind="$1"
  local prefix path

  IGNORE_PREFIXES=()
  IGNORE_EXACT_MAP=()

  for prefix in "${BUILTIN_IGNORE_PREFIXES[@]}"; do
    append_unique_prefix "$prefix"
  done

  case "$repo_kind" in
    src)
      for path in "${BUILTIN_SRC_EXACT_IGNORES[@]}"; do
        set_exact_ignore "$path"
      done
      ;;
    arkweb)
      for path in "${BUILTIN_ARKWEB_EXACT_IGNORES[@]}"; do
        set_exact_ignore "$path"
      done
      ;;
  esac
}

path_is_ignored() {
  [[ "$SHOW_ALL" -eq 1 ]] && return 1
  local path
  path="$(normalize_path "$1")"
  local prefix
  for prefix in "${IGNORE_PREFIXES[@]:-}"; do
    if is_prefixed_path "$path" "$prefix"; then
      return 0
    fi
  done
  [[ -n "${IGNORE_EXACT_MAP[$path]+x}" ]] && return 0
  return 1
}

status_line_is_relevant() {
  local line="$1"
  local payload path_before path_after
  payload="$(normalize_path "${line:3}")"
  if [[ "$payload" == *" -> "* ]]; then
    path_before="${payload%% -> *}"
    path_after="${payload##* -> }"
    if ! path_is_ignored "$path_before"; then
      return 0
    fi
    if ! path_is_ignored "$path_after"; then
      return 0
    fi
    return 1
  fi
  ! path_is_ignored "$payload"
}

print_filtered_status() {
  local repo_root="$1"
  local label="$2"
  local line found=0 ignored=0
  echo "$label status:"
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    if status_line_is_relevant "$line"; then
      echo "$line"
      found=1
    else
      ignored=1
    fi
  done < <(git -C "$repo_root" status --short -uall)
  if [[ "$found" -eq 0 ]]; then
    echo "(no relevant status entries after ignore filtering)"
  fi
  echo
  if [[ "$SHOW_ALL" -eq 0 && "$ignored" -eq 1 ]]; then
    echo "$label ignored default dirty status entries:"
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      if ! status_line_is_relevant "$line"; then
        echo "$line"
      fi
    done < <(git -C "$repo_root" status --short -uall)
    echo
  fi
}

print_filtered_diff_stat() {
  local repo_root="$1"
  local label="$2"
  local diff_mode="$3"
  local -a names=()
  local path
  if [[ "$SHOW_ALL" -eq 1 || "$diff_mode" == "--cached" ]]; then
    echo "$label:"
    if git -C "$repo_root" diff $diff_mode --quiet; then
      echo "(no diff entries)"
    else
      git -C "$repo_root" diff $diff_mode --stat
    fi
    echo
    return 0
  fi
  while IFS= read -r path; do
    [[ -z "$path" ]] && continue
    if ! path_is_ignored "$path"; then
      names+=("$path")
    fi
  done < <(git -C "$repo_root" diff $diff_mode --name-only)
  echo "$label:"
  if [[ "${#names[@]}" -eq 0 ]]; then
    echo "(no relevant diff entries after ignore filtering)"
  else
    git -C "$repo_root" diff $diff_mode --stat -- "${names[@]}"
  fi
  echo
  local -a ignored_names=()
  while IFS= read -r path; do
    [[ -z "$path" ]] && continue
    if path_is_ignored "$path"; then
      ignored_names+=("$path")
    fi
  done < <(git -C "$repo_root" diff $diff_mode --name-only)
  if [[ "${#ignored_names[@]}" -gt 0 ]]; then
    echo "$label ignored default dirty diff entries:"
    printf '%s\n' "${ignored_names[@]}"
    echo
  fi
}

show_repo_changes() {
  local repo_root="$1"
  local label="$2"
  local repo_kind="$3"
  load_builtin_ignores "$repo_kind"
  echo "== $label =="
  echo "Repo: $repo_root"
  echo
  print_filtered_status "$repo_root" "$label"
  print_filtered_diff_stat "$repo_root" "$label unstaged diff --stat" ""
  print_filtered_diff_stat "$repo_root" "$label staged diff --stat" "--cached"
}

ROOT_HINT="$PWD"
for arg in "$@"; do
  case "$arg" in
    --show-all|--no-ignore)
      SHOW_ALL=1
      ;;
    *)
      ROOT_HINT="$arg"
      ;;
  esac
done

ARKWEB_ROOT="$(find_arkweb_root "$ROOT_HINT")"
SRC_REPO="$ARKWEB_ROOT/src"
ARKWEB_REPO="$ARKWEB_ROOT/src/arkweb"

if ! git -C "$SRC_REPO" rev-parse --git-dir >/dev/null 2>&1; then
  echo "src repo not found: $SRC_REPO" >&2
  exit 1
fi

if ! git -C "$ARKWEB_REPO" rev-parse --git-dir >/dev/null 2>&1; then
  echo "arkweb repo not found: $ARKWEB_REPO" >&2
  exit 1
fi

show_repo_changes "$SRC_REPO" "src repo relevant changes" "src"
show_repo_changes "$ARKWEB_REPO" "arkweb repo relevant changes" "arkweb"
if [[ "$SHOW_ALL" -eq 0 ]]; then
  echo "Tip: rerun with --show-all to disable default dirty-file filtering."
fi
