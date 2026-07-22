#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
init_common
detect_build_dir "$STATIC_CORE"

REPO_TO_CHECK=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    log)
      USE_LOG=1
      shift
      ;;
    --repo)
      if [[ -z "${2:-}" ]]; then
        echo "format.sh: --repo requires a repo name (ets_frontend, runtime_core, or all)" >&2
        exit 1
      fi
      REPO_TO_CHECK="$2"
      shift 2
      ;;
    --repo=*)
      REPO_TO_CHECK="${1#--repo=}"
      shift
      ;;
    *)
      echo "format.sh: unknown argument: $1" >&2
      echo "Usage: format.sh [--repo <repo>] [log]" >&2
      echo "  --repo: which repo to check (ets_frontend, runtime_core, or all). Default: all" >&2
      echo "  log: check last commit instead of working tree" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$REPO_TO_CHECK" ]]; then
  REPO_TO_CHECK="all"
fi

clang_format_path="$STATIC_CORE/scripts/code_style/run_code_style_tools.sh"
clang_tidy_path="$STATIC_CORE/scripts/clang-tidy/clang_tidy_check.py"

get_modified_files() {
    local repo_dir="$1"
    local use_log="$2"
    pushd "$repo_dir" > /dev/null
    if [[ -n "$use_log" ]]; then
        local latest_commit
        latest_commit=$(git log -1 --pretty=format:"%H")
        git diff-tree --no-commit-id --name-only -r "$latest_commit"
    else
        git status --porcelain | awk '/^[ M|A]/ {print $2}'
    fi
    popd > /dev/null
}

declare -a all_cpp_files=()

check_repo() {
    local repo_dir="$1"
    local repo_name
    repo_name="$(basename "$repo_dir")"

    if [[ ! -d "$repo_dir/.git" ]]; then
        echo "WARNING: $repo_dir is not a git repository, skipping." >&2
        return
    fi

    echo "=== Checking format for $repo_name ==="

    local modified_files
    modified_files=$(get_modified_files "$repo_dir" "${USE_LOG:-}")

    if [[ -z "$modified_files" ]]; then
        echo "No modified .cpp/.h files found in $repo_name."
        return
    fi

    local cpp_files=()
    while IFS= read -r file; do
        if [[ "$file" == *".cpp" || "$file" == *".h" ]]; then
            cpp_files+=("$file")
            all_cpp_files+=("$repo_dir/$file")
        fi
    done <<< "$modified_files"

    if [[ ${#cpp_files[@]} -eq 0 ]]; then
        echo "No modified .cpp/.h files found in $repo_name."
        return
    fi

    for file in "${cpp_files[@]}"; do
        echo "Running clang-format on $repo_name/$file"
        bash "$clang_format_path" "$repo_dir/$file"
    done

    local filename_filter=""
    for file in "${cpp_files[@]}"; do
        if [[ -n "$filename_filter" ]]; then
            filename_filter+="|"
        fi
        filename_filter+="$file"
    done

    if [[ -n "$filename_filter" ]]; then
        echo "Running clang-tidy on $repo_name files"
        python3 "$clang_tidy_path" "$STATIC_CORE" "$BUILD_DIR" --filename-filter "$filename_filter"
    fi
}

case "$REPO_TO_CHECK" in
    ets_frontend)
        check_repo "$ROOT_DIR/ets_frontend"
        ;;
    runtime_core)
        check_repo "$ROOT_DIR/runtime_core"
        ;;
    all)
        check_repo "$ROOT_DIR/ets_frontend"
        check_repo "$ROOT_DIR/runtime_core"
        ;;
    *)
        echo "format.sh: unknown repo '$REPO_TO_CHECK'. Use ets_frontend, runtime_core, or all." >&2
        exit 1
        ;;
esac

echo "=== Format check completed ==="
