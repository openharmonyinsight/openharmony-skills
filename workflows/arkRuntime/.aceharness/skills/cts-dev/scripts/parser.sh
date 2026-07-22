#!/usr/bin/env bash
set -x
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/common.sh"
init_common
detect_build_dir "$STATIC_CORE"

EXTRA_RUNNER_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --test-file)
      if [[ -z "${2:-}" ]]; then
        echo "parser.sh: --test-file requires a file path" >&2
        exit 1
      fi
      EXTRA_RUNNER_ARGS+=(--test-file "$2")
      shift 2
      ;;
    --test-file=*)
      EXTRA_RUNNER_ARGS+=("$1")
      shift
      ;;
    *)
      echo "parser.sh: unknown argument: $1" >&2
      echo "Usage: parser.sh [--test-file <path> | --test-file=<path>]" >&2
      echo "  <path> is relative to ets2panda/test, e.g. ast/compiler/ets/ambient_declaration.ets" >&2
      exit 1
      ;;
  esac
done

export ARKCOMPILER_RUNTIME_CORE_PATH="$ROOT_DIR/runtime_core"
export ARKCOMPILER_ETS_FRONTEND_PATH="$ROOT_DIR/ets_frontend"
export PANDA_BUILD="$BUILD_DIR"

export WORK_DIR="$ROOT_DIR/work_dir_parser"
rm -rf "$WORK_DIR"
"$ARKCOMPILER_RUNTIME_CORE_PATH/static_core/tests/tests-u-runner-2/runner.sh" es2panda-verifier parser \
  --extension=ets --load-runtimes=ets --force-generate \
  --es2panda-timeout=120 --report-dir report-parser --processes "$(nproc)" \
  "${EXTRA_RUNNER_ARGS[@]}"
