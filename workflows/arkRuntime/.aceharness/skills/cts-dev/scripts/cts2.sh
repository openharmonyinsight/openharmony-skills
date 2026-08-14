#!/usr/bin/env bash
set -x
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
init_common
detect_build_dir_name "$STATIC_CORE"

EXTRA_RUNNER_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --test-file)
      if [[ -z "${2:-}" ]]; then
        echo "cts2.sh: --test-file requires a file path" >&2
        exit 1
      fi
      EXTRA_RUNNER_ARGS+=(--filter "*$2*")
      shift 2
      ;;
    --test-file=*)
      tf="${1#--test-file=}"
      EXTRA_RUNNER_ARGS+=(--filter "*${tf}*")
      shift
      ;;
    --filter)
      if [[ -z "${2:-}" ]]; then
        echo "cts2.sh: --filter requires a filter pattern" >&2
        exit 1
      fi
      EXTRA_RUNNER_ARGS+=(--filter "$2")
      shift 2
      ;;
    --filter=*)
      EXTRA_RUNNER_ARGS+=("$1")
      shift
      ;;
    *)
      echo "cts2.sh: unknown argument: $1" >&2
      echo "Usage: cts2.sh [--test-file <path>] [--filter <pattern>]" >&2
      echo "  --test-file: CTS test path, e.g. 17.experimental_features/13.adding_functionality_to_existing_types/04.function_types_with_receiver/function_types_with_receiver" >&2
      echo "  --filter:    Runner filter pattern, e.g. '*13.adding_functionality_to_existing_types*'" >&2
      exit 1
      ;;
  esac
done

cd "$STATIC_CORE"
tests/tests-u-runner/runner.sh --ets-cts --show-progress --build-dir "$BUILD_DIR" --processes=all --es2panda-debug-info --force-generate --es2panda-args=--simultaneous=true "${EXTRA_RUNNER_ARGS[@]}"
