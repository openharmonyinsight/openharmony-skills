#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

PROJECT_ROOT="$TMP_ROOT/project"
STATIC_CORE="$PROJECT_ROOT/runtime_core/static_core"
EXTERNAL_BUILD_DIR="$TMP_ROOT/external/ark-out"
RUNNER_LOG="$TMP_ROOT/runner.log"
CMAKE_LOG="$TMP_ROOT/cmake.log"
BIN_DIR="$TMP_ROOT/bin"

mkdir -p "$STATIC_CORE/tests/tests-u-runner"
mkdir -p "$STATIC_CORE/scripts"
mkdir -p "$STATIC_CORE/tools"
mkdir -p "$EXTERNAL_BUILD_DIR/bin"
mkdir -p "$PROJECT_ROOT/ets_frontend"
mkdir -p "$BIN_DIR"

cat > "$STATIC_CORE/tests/tests-u-runner/runner.sh" <<'RUNNER'
#!/usr/bin/env bash
for arg in "$@"; do
    case "$arg" in
        --workdir=*)
            mkdir -p "${arg#*=}"
            touch "${arg#*=}/runner-was-here"
            ;;
    esac
done
printf '%s\n' "$*" > "$RUNNER_LOG"
RUNNER
chmod +x "$STATIC_CORE/tests/tests-u-runner/runner.sh"

cat > "$STATIC_CORE/scripts/install-third-party" <<'INSTALL'
#!/usr/bin/env bash
exit 0
INSTALL
chmod +x "$STATIC_CORE/scripts/install-third-party"

cat > "$BIN_DIR/cmake" <<'CMAKE'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$CMAKE_LOG"
CMAKE
chmod +x "$BIN_DIR/cmake"

export ARK_ROOT_DIR="$PROJECT_ROOT"
export ARK_BUILD_DIR="$EXTERNAL_BUILD_DIR"
export RUNNER_LOG
export CMAKE_LOG

"$SCRIPT_DIR/cts2.sh" --filter smoke

grep -q -- "--build-dir $EXTERNAL_BUILD_DIR " "$RUNNER_LOG" || {
    echo "cts2.sh did not pass absolute ARK_BUILD_DIR to runner" >&2
    cat "$RUNNER_LOG" >&2
    exit 1
}

"$SCRIPT_DIR/runtime.sh"

grep -q -- "--build-dir $EXTERNAL_BUILD_DIR " "$RUNNER_LOG" || {
    echo "runtime.sh did not pass absolute ARK_BUILD_DIR to runner" >&2
    cat "$RUNNER_LOG" >&2
    exit 1
}

RUNTIME_WORKDIR="$(sed -n 's/.*--workdir=\([^ ]*\).*/\1/p' "$RUNNER_LOG")"
[[ -n "$RUNTIME_WORKDIR" && "$RUNTIME_WORKDIR" != "/tmp/ets" ]] || {
    echo "runtime.sh did not pass a run-scoped workdir to runner" >&2
    cat "$RUNNER_LOG" >&2
    exit 1
}

[[ ! -e "$RUNTIME_WORKDIR/runner-was-here" ]] || {
    echo "runtime.sh did not clean its run-scoped workdir" >&2
    exit 1
}

grep -Eq -- "--workdir=/tmp/ets($| )" "$RUNNER_LOG" && {
    echo "runtime.sh passed the fixed global /tmp/ets workdir" >&2
    cat "$RUNNER_LOG" >&2
    exit 1
}

PATH="$BIN_DIR:$PATH" "$SCRIPT_DIR/install_build.sh"

grep -q -- "-B $EXTERNAL_BUILD_DIR " "$CMAKE_LOG" || {
    echo "install_build.sh did not pass absolute ARK_BUILD_DIR to cmake -B" >&2
    cat "$CMAKE_LOG" >&2
    exit 1
}

grep -q -- "--build $EXTERNAL_BUILD_DIR" "$CMAKE_LOG" || {
    echo "install_build.sh did not pass absolute ARK_BUILD_DIR to cmake --build" >&2
    cat "$CMAKE_LOG" >&2
    exit 1
}
