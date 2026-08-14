#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

PROJECT_ROOT="$TMP_ROOT/project"
STATIC_CORE="$PROJECT_ROOT/runtime_core/static_core"
FRONTEND="$PROJECT_ROOT/ets_frontend"
BUILD_DIR="$STATIC_CORE/out"
FORMAT_LOG="$TMP_ROOT/format.log"
TIDY_LOG="$TMP_ROOT/tidy.log"

mkdir -p "$STATIC_CORE/scripts/code_style"
mkdir -p "$STATIC_CORE/scripts/clang-tidy"
mkdir -p "$BUILD_DIR/bin"
mkdir -p "$FRONTEND"

cat > "$STATIC_CORE/scripts/code_style/run_code_style_tools.sh" <<'FORMAT'
#!/usr/bin/env bash
printf '%s\n' "$1" >> "$FORMAT_LOG"
FORMAT
chmod +x "$STATIC_CORE/scripts/code_style/run_code_style_tools.sh"

cat > "$STATIC_CORE/scripts/clang-tidy/clang_tidy_check.py" <<'TIDY'
#!/usr/bin/env python3
import os
import sys
with open(os.environ["TIDY_LOG"], "a", encoding="utf-8") as out:
    out.write(" ".join(sys.argv[1:]) + "\n")
TIDY
chmod +x "$STATIC_CORE/scripts/clang-tidy/clang_tidy_check.py"

cd "$FRONTEND"
/usr/bin/git init -q
/usr/bin/git config user.email test@example.com
/usr/bin/git config user.name test

printf 'int main() { return 0; }\n' > modified.cpp
printf 'int deleted() { return 0; }\n' > deleted.cpp
/usr/bin/git add modified.cpp deleted.cpp
/usr/bin/git commit -q -m init

printf 'int main() { return 1; }\n' > modified.cpp
rm deleted.cpp
printf 'int new_file() { return 0; }\n' > new.cpp

export ARK_ROOT_DIR="$PROJECT_ROOT"
export ARK_BUILD_DIR="$BUILD_DIR"
export FORMAT_LOG
export TIDY_LOG
export GIT_BIN=/usr/bin/git

"$SCRIPT_DIR/format.sh" --repo ets_frontend

grep -q '/modified.cpp$' "$FORMAT_LOG" || {
    echo "modified.cpp was not formatted" >&2
    cat "$FORMAT_LOG" >&2
    exit 1
}

grep -q '/new.cpp$' "$FORMAT_LOG" || {
    echo "untracked new.cpp was not formatted" >&2
    cat "$FORMAT_LOG" >&2
    exit 1
}

if grep -q '/deleted.cpp$' "$FORMAT_LOG"; then
    echo "deleted.cpp should not be formatted" >&2
    cat "$FORMAT_LOG" >&2
    exit 1
fi
